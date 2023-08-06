import argparse
import time
from itertools import chain
from pathlib import Path
import sys

import torch
import torch.nn as nn
import torch.utils.data
from kaldialign import edit_distance, align
import wandb

from .data import concat_datasets
from .beam import ctc_beam_search_decode_logits
from .model import Encoder, CTCRecognizer, StarRecognizer
from .resnet import FixupResNet, FixupBasicBlock
from .xen import Vocabulary
from . import symbol_tape
from .rnnlm import LM
from .transducer import transducer_forward_score
from .ctc import ctc_reduce_mean


def log(*args, flush=False, **kwargs):
    print(*args, **kwargs, flush=flush, file=sys.stderr)


class Collator:
    def __init__(self, vocabulary):
        self.vocabulary = vocabulary

    def __call__(self, batch):
        batch_indices = torch.tensor([b[0] for b in batch])
        input_lengths = torch.tensor([len(b[1]) for b in batch])
        inputs = torch.nn.utils.rnn.pad_sequence([b[1] for b in batch], batch_first=True)
        targets = [self.vocabulary.encode(b[2]) for b in batch]
        target_lengths = torch.tensor([len(t) for t in targets])
        targets = torch.nn.utils.rnn.pad_sequence(targets, batch_first=True, padding_value=-100)
        return batch_indices, inputs, targets, input_lengths, target_lengths


def make_vocab(vocab_descriptor):
    match vocab_descriptor.split(':', maxsplit=1):
        case ["bytes"]:
            return symbol_tape.Vocabulary.bytes()
        case ["ascii"]:
            return symbol_tape.Vocabulary.ascii()
        case ["cmu"]:
            return Vocabulary(add_closures=False)
        case ["xen"]:
            return Vocabulary(add_closures=True)
        case ["words", path]:
            _, vocab = symbol_tape.tokenize_words(path, None)
            return vocab
        case _:
            raise ValueError("Unknown vocabulary descriptor. Possible values: bytes|ascii|cmu|xen|words:path/to/vocab/words.txt")


class System(nn.Module):
    def __init__(self, args):
        super().__init__()
        self.args = args

        match args.encoder:
            case "lstm":
                self.encoder = Encoder().to(args.device)
            case "r9":
                self.encoder = FixupResNet(FixupBasicBlock, [5,5,5]).to(args.device)

        self.vocab = make_vocab(args.vocab)

        match args.star_penalty:
            case None:
                self.recognizer = CTCRecognizer(vocab_size=len(self.vocab)).to(args.device)
            case star_penalty:
                self.recognizer = StarRecognizer(star_penalty=star_penalty,
                                                 vocab_size=len(self.vocab)).to(args.device)    

        if args.lm:
            lm_checkpoint = torch.load(args.lm, map_location=args.device)
            self.lm_args = lm_checkpoint['args']
            self.lm = LM(vocab_size=len(self.vocab),
                         emb_dim=self.lm_args['rnn_size'],
                         hidden_dim=self.lm_args['rnn_size'],
                         num_layers=self.lm_args['num_layers'],
                         dropout=self.lm_args['dropout']).to(args.device)
            #self.lm.load_state_dict(lm_checkpoint['model'])

            self.optimizer = torch.optim.Adam(chain(self.encoder.parameters(),
                                                    self.recognizer.parameters(),
                                                    self.lm.parameters()), lr=args.lr)
        else:
            self.lm_args, self.lm = None, None

            self.optimizer = torch.optim.Adam(chain(self.encoder.parameters(),
                                                    self.recognizer.parameters()), lr=args.lr)
        self.scaler = torch.cuda.amp.GradScaler()

    def load_state_dict(self, checkpoint):
        self.encoder.load_state_dict(checkpoint['encoder'])
        self.recognizer.load_state_dict(checkpoint['recognizer'])
        self.scaler.load_state_dict(checkpoint['scaler'])
        self.optimizer.load_state_dict(checkpoint['optimizer'])
        self.vocab.load_state_dict(checkpoint['vocab'])
        if self.lm is not None:
            log('loading transducer lm')
            self.lm.load_state_dict(checkpoint['lm'])

    def make_state_dict(self, **extra):
        return {
            'encoder': self.encoder.state_dict(),
            'recognizer': self.recognizer.state_dict(),
            'scaler': self.scaler.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'vocab': self.vocab.state_dict(),
            'lm_args': self.lm_args,
            'lm': self.lm.state_dict() if self.lm is not None else None,
        } | extra

    def forward(self, inputs, targets, input_lengths, target_lengths):
        device = self.args.device

        N, _, _ = inputs.shape
        inputs = inputs.to(device) # (N, T, C)
        targets = targets.to(device) # (N, U)
        input_lengths = input_lengths.to(device) # (N,)
        target_lengths = target_lengths.to(device) # (N,)

        #log(inputs, targets) # works best with --batch-size 1

        input_lengths = self.encoder.subsampled_lengths(input_lengths)

        with torch.autocast(device_type='cuda', dtype=torch.float16):
            outputs = self.encoder(inputs) # (N1, T, C)

            if self.lm is not None:
                #
                # Output dependencies are controller by LM
                #
                hidden = self.lm.init_hidden(N)

                # input needs to start with 0
                lm_targets = torch.cat([targets.new_zeros((N, 1)), targets], dim=1) # (N, U1)

                lm_outputs, _ = self.lm.forward_batch_first(lm_targets, hidden) # (N, U1, C)

                outputs = self.recognizer.dropout(outputs)
                outputs = self.recognizer.classifier(outputs) # (N, T, C)

                joint = outputs[:, :, None, :] + lm_outputs[:, None, :, :] # (N, T, U1, C)
                #joint = joint.log_softmax(dim=-1)

                #loss = ctc_reduce_mean(transducer_forward_score(joint, targets, input_lengths, target_lengths), target_lengths)

                from torchaudio.functional import rnnt_loss
                loss = rnnt_loss(joint,
                                 targets.to(torch.int32),
                                 input_lengths.to(torch.int32),
                                 target_lengths.to(torch.int32),
                                 blank=0, reduction='mean', fused_log_softmax=True)
                logits = joint # FIXME:
            else:
                #
                # All outputs are independent
                #
                loss, logits = self.recognizer(outputs, targets, input_lengths, target_lengths)

        return loss, outputs, logits

    def train_one_epoch(self, epoch, train_loader):
        encoder, recognizer, optimizer, scaler = self.encoder, self.recognizer, self.optimizer, self.scaler

        optimizer.zero_grad()
        encoder.train()
        recognizer.train()

        train_loss = 0.
        t0 = time.time()
        for i, (_batch_indices, inputs, targets, input_lengths, target_lengths) in enumerate(train_loader):
            loss, _, _ = self.forward(inputs, targets, input_lengths, target_lengths)

            if torch.isnan(loss):
                log(f'[{epoch + 1}, {i + 1:5d}], loss is nan, skipping batch', flush=True)
                scaler.update()
                continue

            if torch.isinf(loss):
                log(f'[{epoch + 1}, {i + 1:5d}], loss is inf, skipping batch, skipping scaler update', flush=True)
                continue

            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            grad_norm = torch.nn.utils.clip_grad_norm_(chain(encoder.parameters(), recognizer.parameters()), self.args.clip_grad_norm)
            if self.lm:
                grad_norm = 0.5*(grad_norm + torch.nn.utils.clip_grad_norm_(self.lm.parameters(), self.args.clip_grad_norm))
            if torch.isinf(grad_norm) or torch.isnan(grad_norm):
                log(f'[{epoch + 1}, {i + 1:5d}], grad_norm is inf or nan, skipping batch', flush=True)
                scaler.update()
                optimizer.zero_grad(set_to_none=True)
                continue

            scaler.step(optimizer)
            scaler.update()
            optimizer.zero_grad(set_to_none=True)

            train_loss += loss.item()
            if i and i % self.args.log_interval == 0:
                train_loss = train_loss / self.args.log_interval
                t1 = time.time()
                log(f'[{epoch + 1}, {i + 1:5d}] time: {t1-t0:.3f} loss: {train_loss:.3f} grad_norm: {grad_norm:.3f}', flush=True)
                wandb.log({'train/loss': train_loss, 'train/grad_norm': grad_norm})
                t0 = t1
                train_loss = 0.

    @torch.inference_mode()
    def evaluate(self, epoch, valid_loader):
        encoder, recognizer, vocabulary = self.encoder, self.recognizer, self.vocab

        valid_loss = 0.
        lers = []

        encoder.eval()
        recognizer.eval()
        for i, (dataset_indices, inputs, targets, input_lengths, target_lengths) in enumerate(valid_loader):
            loss, outputs, logits = self.forward(inputs, targets, input_lengths, target_lengths)

            valid_loss += loss.item()

            for dataset_index, ref, ref_len, seq, hyp_len in zip(dataset_indices, targets, target_lengths, logits, input_lengths):
                seq = seq[:hyp_len].cpu()
                ref = ref[:ref_len].cpu().tolist()
                ali = seq.argmax(dim=-1)

                greedy = [i for i in torch.unique_consecutive(ali, dim=-1).tolist() if i]
                hyp1 = vocabulary.decode(greedy)

                #decoded_seqs, _decoded_logits = ctc_beam_search_decode_logits(seq) # FIXME: too slow
                #hyp1 = vocabulary.decode(filter(None, decoded_seqs[0]))

                ref1 = vocabulary.decode(ref)
                ali = vocabulary.decode(ali.tolist())

                dist = edit_distance(hyp1, ref1)
                dist['length'] = len(ref1)
                dist['ler'] = round(dist['total'] / dist['length'], 2)
                lers.append(dist['ler'])

                if isinstance(ref1, list):
                    star = '␣'
                    hyp, ref = list(zip(*align(hyp1, ref1, star)))
                    ali = tuple(ali)
                elif isinstance(ref1, str):
                    star = '␣'
                    hyp, ref = list(zip(*align(hyp1, ref1, star)))
                    hyp, ref = ''.join(hyp), ''.join(ref)
                else:
                    star = 42 # b'*'
                    hyp, ref = list(zip(*align(hyp1, ref1, star)))
                    hyp, ref = bytes(hyp), bytes(ref)

                dataset_index = dataset_index.item()
                print(epoch, dataset_index, 'hyp', self.vocab.format(hyp), sep="\t", flush=True)
                print(epoch, dataset_index, 'ref', self.vocab.format(ref), sep="\t", flush=True)
                print(epoch, dataset_index, 'ali', self.vocab.format(ali), sep="\t", flush=True)
                print(epoch, dataset_index, 'stat', dist, sep="\t", flush=True)

        count = i + 1
        ler = round(sum(lers) / len(lers), 3)
        log(f'valid [{epoch + 1}, {i + 1:5d}] loss: {valid_loss / count:.3f} ler: {ler:.3f}', flush=True)
        if wandb.run is not None:
            wandb.log({'valid/loss': valid_loss / count, 'valid/ler': ler})
        return valid_loss / count


def make_parser():
    class Formatter(argparse.ArgumentDefaultsHelpFormatter,
                    argparse.MetavarTypeHelpFormatter):
        pass

    parser = argparse.ArgumentParser(formatter_class=Formatter)
    parser.add_argument('--init', type=Path, help="Path to checkpoint to initialize from")
    parser.add_argument('--save', type=Path, default='ckpt.pt', help="Path to save checkpoint to")
    parser.add_argument('--log-interval', type=int, default=100, help="Number of batches between printing training status")
    parser.add_argument('--num-epochs', type=int, default=30, help="Number of epochs to train for")
    parser.add_argument('--device', type=str, default='cuda:1', help="torch device to use")
    parser.add_argument('--batch-size', type=int, default=16, help="Batch size")
    parser.add_argument('--lr', type=float, default=3e-4, help="Adam learning rate")
    parser.add_argument('--train', type=str, help="Datasets to train on, comma separated")
    parser.add_argument('--eval', type=str, default='dev-clean', help="Datasets to evaluate on, comma separated")
    parser.add_argument('--encoder', type=str, default='lstm', choices=['lstm', 'r9'], help="Encoder to use: unidirectional LSTM or ResNet")
    parser.add_argument('--compile', action='store_true', help="torch.compile the model (produces incompatible checkpoints)")
    parser.add_argument('--star-penalty', type=float, default=None, help="Star penalty for Star CTC. If None, train with regular CTC")
    parser.add_argument('--num-workers', type=int, default=32, help="Number of workers for data loading")
    parser.add_argument('--vocab', type=str, default='ascii', help="Vocabulary to use: bytes|ascii|cmu|xen|words:path/to/words.txt")
    parser.add_argument('--lm', type=Path, help="Path to language model checkpoint trained with hal.")
    parser.add_argument('--clip-grad-norm', type=float, default=0.1, help="Clip gradient norm to this value")
    return parser


def main():
    args = make_parser().parse_args()
    log(args)

    torch.manual_seed(3407)

    system = System(args)

    valid_loader = torch.utils.data.DataLoader(
        concat_datasets(args.eval),
        collate_fn=Collator(system.vocab),
        batch_size=16,
        shuffle=False,
        num_workers=args.num_workers,
    )

    if args.init:
        checkpoint = torch.load(args.init, map_location=args.device)
        system.load_state_dict(checkpoint)
    else:
        log('initializing randomly')

    if args.compile:
        system = torch.compile(system, mode='reduce-overhead')

    log('model parameters', sum(p.numel() for p in system.parameters() if p.requires_grad))

    if args.train:
        wandb.init(project='ha', config=args)

        train_loader = torch.utils.data.DataLoader(
            concat_datasets(args.train),
            collate_fn=Collator(system.vocab),
            batch_size=args.batch_size,
            shuffle=True,
            num_workers=args.num_workers,
            drop_last=True
        )

        best_valid_loss = float('inf')
        for epoch in range(args.num_epochs):
            system.train_one_epoch(epoch, train_loader)

            valid_loss = system.evaluate(epoch, valid_loader)
            if valid_loss < best_valid_loss:
                best_valid_loss = valid_loss
                log('saving model', args.save)
                torch.save(system.make_state_dict(best_valid_loss=best_valid_loss, epoch=epoch), args.save)
    else:
        system.evaluate(-100, valid_loader)

if __name__ == '__main__':
    main()
