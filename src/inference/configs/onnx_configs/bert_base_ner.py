import numpy as np


def get_slice_inputs(tokenized_sentence):
    slice_input = {
        'input_ids': np.ascontiguousarray(tokenized_sentence['input_ids'].cpu().numpy()),
        'attention_mask': np.ascontiguousarray(tokenized_sentence['attention_mask'].cpu().numpy()),
        'token_type_ids': np.ascontiguousarray(tokenized_sentence['token_type_ids'].cpu().numpy()),
    }
    return slice_input


def decode(tokenizer, tokenized_sentence, model_output):
    label_indices = np.argmax(model_output[0], axis=2)
    tokens = tokenizer.convert_ids_to_tokens(tokenized_sentence['input_ids'][0])

    return tokens, label_indices
