from transformers import GPT2LMHeadModel, GPT2Tokenizer

from model_handler import ModelHandler


MAX_TEXT_LEN = 70  # maximum number of words in output text
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')


class Gpt2(ModelHandler):
    def set_model_weights(self, **kwargs):
        self.weights = None
        self.pretrained = True

    def create_model(self, **kwargs):
        return GPT2LMHeadModel.from_pretrained('gpt2', pad_token_id=tokenizer.eos_token_id)


def gpt_text_generation(gpt_model, input_promt, device):
    input_ids = tokenizer.encode(input_promt, return_tensors='pt').to(device)

    # Basic Sampling decoding method
    sample_output = gpt_model.generate(
        input_ids,
        do_sample=True,
        max_length=MAX_TEXT_LEN,
        top_k=0,
        temperature=0.8,
    )
    decoded_output = tokenizer.decode(sample_output[0], skip_special_tokens=True)

    return decoded_output
