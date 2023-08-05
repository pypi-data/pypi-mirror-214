import torch

from tqdm import tqdm

from primeqa.ir.dense.colbert_top.colbert.modeling.tokenization import QueryTokenizer, DocTokenizer
from primeqa.ir.dense.colbert_top.colbert.utils.amp import MixedPrecisionManager

from primeqa.ir.dense.colbert_top.colbert.modeling.colbert import ColBERT
from primeqa.ir.dense.colbert_top.colbert.utils.utils import torch_load_dnn
from primeqa.ir.dense.colbert_top.colbert.modeling.factory import get_query_tokenizer, get_doc_tokenizer
from primeqa.ir.dense.colbert_top.colbert.utils.utils import print_message

class Checkpoint(ColBERT):
    """
        Easy inference with ColBERT.

        TODO: Add .cast() accepting [also] an object instance-of(Checkpoint) as first argument.
    """

    def __init__(self, name, colbert_config=None):

        super().__init__(name, colbert_config)
        assert self.training is False

        # get model type from checkpoint
        if name.endswith('.dnn') or name.endswith('.model'):
            dnn_checkpoint = torch_load_dnn(colbert_config.checkpoint)
            model_type = dnn_checkpoint['model_type']
        else:
            model_type=name

        self.query_tokenizer = get_query_tokenizer(model_type, colbert_config.query_maxlen, colbert_config.attend_to_mask_tokens)
        self.doc_tokenizer = get_doc_tokenizer(model_type, colbert_config.doc_maxlen)

        self.amp_manager = MixedPrecisionManager(True)

        self.docFromText_used = False

    def query(self, *args, to_cpu=False, **kw_args):
        with torch.no_grad():
            with self.amp_manager.context():
                Q = super().query(*args, **kw_args)
                return Q.cpu() if to_cpu else Q

    def doc(self, *args, to_cpu=False, **kw_args):
        with torch.no_grad():
            with self.amp_manager.context():
                D = super().doc(*args, **kw_args)

                if to_cpu:
                    return (D[0].cpu(), *D[1:]) if isinstance(D, tuple) else D.cpu()

                return D

    def queryFromText(self, queries, bsize=None, to_cpu=False, context=None):
        if bsize:
            batches = self.query_tokenizer.tensorize(queries, context=context, bsize=bsize)
            batches = [self.query(input_ids, attention_mask, to_cpu=to_cpu) for input_ids, attention_mask in batches]
            return torch.cat(batches)

        input_ids, attention_mask = self.query_tokenizer.tensorize(queries, context=context)
        return self.query(input_ids, attention_mask)

    def docFromText(self, docs, bsize=None, keep_dims=True, to_cpu=False, showprogress=False, return_tokens=False):
        assert keep_dims in [True, False, 'flatten']

        if not self.docFromText_used:
            print_message(f"#> checkpoint, docFromText, Input: {docs[0]}, \t\t {bsize}")

        if bsize:
            text_batches, reverse_indices = self.doc_tokenizer.tensorize(docs, bsize=bsize)

            if not self.docFromText_used:
                print_message(f"#> checkpoint, docFromText, Output IDs: {text_batches[0]}")
                self.docFromText_used = True

            returned_text = []
            if return_tokens:
                returned_text = [text for batch in text_batches for text in batch[0]]
                returned_text = [returned_text[idx] for idx in reverse_indices.tolist()]
                returned_text = [returned_text]

            keep_dims_ = 'return_mask' if keep_dims == 'flatten' else keep_dims
            batches = [self.doc(input_ids, attention_mask, keep_dims=keep_dims_, to_cpu=to_cpu)
                       for input_ids, attention_mask in tqdm(text_batches, disable=not showprogress)]

            if keep_dims is True:
                D = _stack_3D_tensors(batches)
                return (D[reverse_indices], *returned_text)

            elif keep_dims == 'flatten':
                D, mask = [], []

                for D_, mask_ in batches:
                    D.append(D_)
                    mask.append(mask_)

                D, mask = torch.cat(D)[reverse_indices], torch.cat(mask)[reverse_indices]

                doclens = mask.squeeze(-1).sum(-1).tolist()

                D = D.view(-1, self.colbert_config.dim)
                D = D[mask.bool().flatten()].cpu()

                return (D, doclens, *returned_text)

            assert keep_dims is False

            D = [d for batch in batches for d in batch]
            return ([D[idx] for idx in reverse_indices.tolist()], *returned_text)

        input_ids, attention_mask = self.doc_tokenizer.tensorize(docs)
        return self.doc(input_ids, attention_mask, keep_dims=keep_dims, to_cpu=to_cpu)

    def lazy_rank(self, queries, docs):
        Q = self.queryFromText(queries, bsize=128, to_cpu=True)
        D = self.docFromText(docs, bsize=128, to_cpu=True)

        assert False, "Implement scoring"

    def score(self, Q, D, mask=None, lengths=None):
        assert False, "Call colbert_score"
        # EVENTUALLY: Just call the colbert_score function!

        if lengths is not None:
            assert mask is None, "don't supply both mask and lengths"

            mask = torch.arange(D.size(1), device=self.device) + 1
            mask = mask.unsqueeze(0) <= lengths.to(self.device).unsqueeze(-1)

        scores = (D @ Q)
        scores = scores if mask is None else scores * mask.unsqueeze(-1)
        scores = scores.max(1)

        return scores.values.sum(-1).cpu()


def _stack_3D_tensors(groups):
    bsize = sum([x.size(0) for x in groups])
    maxlen = max([x.size(1) for x in groups])
    hdim = groups[0].size(2)

    output = torch.zeros(bsize, maxlen, hdim, device=groups[0].device, dtype=groups[0].dtype)

    offset = 0
    for x in groups:
        endpos = offset + x.size(0)
        output[offset:endpos, :x.size(1)] = x
        offset = endpos

    return output


"""
TODO:

def tokenize_and_encode(checkpoint, passages):
    embeddings, token_ids = checkpoint.docFromText(passages, bsize=128, keep_dims=False, showprogress=True, return_tokens=True)
    tokens = [checkpoint.doc_tokenizer.tok.convert_ids_to_tokens(ids.tolist()) for ids in token_ids]
    tokens = [tokens[:tokens.index('[PAD]') if '[PAD]' in tokens else -1] for tokens in tokens]
    tokens = [[tok for tok in tokens if tok not in checkpoint.skiplist] for tokens in tokens]

    return embeddings, tokens

"""
