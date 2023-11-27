import torch

from transformers import AutoTokenizer, AutoModelForCausalLM

from configs.pytorch_configs.model_handler import ModelHandler

MAX_TEXT_LEN = 70  # maximum number of words in output text


class CausalLMBase(ModelHandler):
    def __init__(self, name):
        super().__init__()
        self.set_model_name(name)

    def set_model_weights(self, **kwargs):
        self.weights = None
        self.pretrained = True
        self.use_custom_trace_step = True

    def create_model(self, should_be_traced, trust_remote_code=False, **kwargs):
        tokenizer = create_tokenizer(self.model_name)

        no_cache_args = self.get_no_cache_flags()
        trace_args = self.get_traced_loading_flags() if should_be_traced else {}

        params = dict(pretrained_model_name_or_path=self.model_name,
                      pad_token_id=tokenizer.eos_token_id,
                      trust_remote_code=trust_remote_code,
                      **trace_args, **no_cache_args)

        if kwargs['precision'] == 'BF16':
            params.update({'torch_dtype': torch.bfloat16})
        elif kwargs['precision'] == 'FP16':
            params.update({'torch_dtype': torch.float16})

        return AutoModelForCausalLM.from_pretrained(**params)

    def trace_model(self, model, device, **kwargs):
        tokenizer = create_tokenizer(self.model_name)
        tokens = tokenizer('Test', return_tensors='pt')['input_ids'].to(device)
        traced_model = torch.jit.trace(model, tokens)
        return traced_model


def create_tokenizer(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.padding_side = 'left'
    tokenizer.pad_token = tokenizer.eos_token
    return tokenizer


def tokenize(tokenizer, prompt):
    return tokenizer(prompt, return_tensors='pt', padding=True)


def generate(model, inputs, device):
    return model.generate(
        input_ids=inputs['input_ids'].to(device),
        attention_mask=inputs['attention_mask'].to(device),
        do_sample=True,
        max_length=MAX_TEXT_LEN,
        top_k=0,
        temperature=0.8,
    )


def decode(tokenizer, outputs):
    decoded_outputs = [tokenizer.decode(output, skip_special_tokens=True) for
                       output in outputs]
    return decoded_outputs
