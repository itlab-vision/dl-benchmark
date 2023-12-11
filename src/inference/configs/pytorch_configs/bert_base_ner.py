import numpy as np

from transformers import AutoTokenizer, AutoModelForTokenClassification

from configs.pytorch_configs.model_handler import ModelHandler


BERT_NER_MODEL = 'dslim/bert-base-NER'
CONLL_NER_ID_2TAG = {0: 'O',
                     1: 'B-MISC',
                     2: 'I-MISC',
                     3: 'B-PER',
                     4: 'I-PER',
                     5: 'B-ORG',
                     6: 'I-ORG',
                     7: 'B-LOC',
                     8: 'I-LOC'}


class BertBaseNer(ModelHandler):
    def set_model_weights(self, **kwargs):
        self.weights = None
        self.pretrained = True

    def create_model(self, should_be_traced, **kwargs):
        trace_args = self.get_traced_loading_flags() if should_be_traced else {}
        no_cache_args = self.get_no_cache_flags()
        return AutoModelForTokenClassification.from_pretrained(BERT_NER_MODEL,
                                                               **trace_args, **no_cache_args)


def create_tokenizer():
    return AutoTokenizer.from_pretrained(BERT_NER_MODEL, force_download=True)


def tokenize(tokenizer, prompt):
    return tokenizer(prompt, return_tensors='pt')


def get_decode_result(tokens, label_indices):
    new_tokens, new_labels = [], []
    for token, label_idx in zip(tokens, label_indices[0]):
        if token.startswith('##'):
            new_tokens[-1] = new_tokens[-1] + token[2:]
        else:
            new_labels.append(CONLL_NER_ID_2TAG[label_idx])
            new_tokens.append(token)

    return zip(new_tokens, new_labels)


def decode(tokenizer, tokenized_sentence, model_output):
    label_indices = np.argmax(model_output[0].to('cpu').numpy(), axis=2)
    tokens = tokenizer.convert_ids_to_tokens(tokenized_sentence.to('cpu').numpy()[0])

    return tokens, label_indices
