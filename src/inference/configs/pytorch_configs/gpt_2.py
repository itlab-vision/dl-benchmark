import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

from model_handler import ModelHandler


MAX_TEXT_LEN = 70  # maximum number of words in output text
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
# the lines below are needed to make batch inference work correctly
tokenizer.padding_side = 'left'
tokenizer.pad_token = tokenizer.eos_token


class Gpt2(ModelHandler):
    def set_model_weights(self, **kwargs):
        self.weights = None
        self.pretrained = True
        self.use_custom_trace_step = True

    def create_model(self, should_be_traced, **kwargs):
        trace_args = self.get_traced_loading_flags() if should_be_traced else {}
        no_cache_args = self.get_no_cache_flags()
        return GPT2LMHeadModel.from_pretrained('gpt2', pad_token_id=tokenizer.eos_token_id,
                                               **trace_args, **no_cache_args)

    def trace_model(self, model, device, **kwargs):
        tokens = tokenizer('Test', return_tensors='pt')['input_ids'].to(device)
        traced_model = torch.jit.trace(model, tokens)
        return traced_model


def tokenize(prompt):
    return tokenizer(prompt, return_tensors='pt', padding=True)


def generate(gpt_model, inputs, device):
    return gpt_model.generate(
        input_ids=inputs['input_ids'].to(device),
        attention_mask=inputs['attention_mask'].to(device),
        do_sample=True,
        max_length=MAX_TEXT_LEN,
        top_k=0,
        temperature=0.8,
    )


def decode(outputs):
    decoded_outputs = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
    return decoded_outputs
