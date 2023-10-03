import torch
import numpy


MAX_TEXT_LEN = 70  # maximum number of words in output text


def get_input_dicts(encodings_dict, device):
    input_ids = torch.tensor(encodings_dict['input_ids'], dtype=torch.int32)
    attention_mask = torch.tensor(encodings_dict['attention_mask'], dtype=torch.int32)

    position_ids = attention_mask.long().cumsum(-1) - 1
    position_ids.masked_fill_(position_ids < 0, 0)
    position_ids = position_ids.to(torch.int32)

    past = []

    batch_size = input_ids.size(0)
    # data from model.config
    num_attention_heads = 12
    hidden_size = 768
    num_layer = 12
    past_shape = [2, batch_size, num_attention_heads, 0, hidden_size // num_attention_heads]

    for _ in range(num_layer):
        past.append(torch.empty(past_shape).type(torch.float32).to(device))

    return input_ids.to(device), attention_mask.to(device), position_ids.to(device), past, batch_size, num_layer


def get_slice_inputs(input_ids, attention_mask, position_ids, past):
    slice_input = {
        'input_ids': numpy.ascontiguousarray(input_ids.cpu().numpy()),
        'attention_mask': numpy.ascontiguousarray(attention_mask.cpu().numpy()),
        'position_ids': numpy.ascontiguousarray(position_ids.cpu().numpy()),
    }
    for i, past_i in enumerate(past):
        slice_input[f'past_{i}'] = numpy.ascontiguousarray(past_i.cpu().numpy())

    return slice_input


def batch_text_generation(tokenizer, device, encodings_dict, number_iter=MAX_TEXT_LEN,
                          output_names=None, torch_model=None, ort_session=None):
    use_onnxruntime = ort_session is not None
    if not use_onnxruntime and torch_model is None:
        raise ValueError('onnxruntime session or pytorch model should exist!')

    if device == 'CPU':
        device = torch.device('cpu')
    elif device == 'NVIDIA_GPU':
        device = torch.device('cuda')

    input_ids, attention_mask, position_ids, past, batch_size, num_layer = get_input_dicts(encodings_dict, device)

    eos_token_id = tokenizer.eos_token_id
    has_eos = torch.zeros(batch_size, dtype=torch.bool, device=device)

    all_token_ids = input_ids.clone()

    for _ in range(number_iter):
        if use_onnxruntime:
            slice_input = get_slice_inputs(input_ids, attention_mask, position_ids, past)
            result = ort_session.run(output_names, slice_input)
        else:
            result = torch_model(input_ids, attention_mask=attention_mask, position_ids=position_ids,
                                 past_key_values=past)

        next_token_logits = result[0][:, -1, :]
        if use_onnxruntime:
            next_token_logits = torch.from_numpy(next_token_logits).to(device)
        next_tokens = torch.argmax(next_token_logits, dim=-1).to(device)

        # updates which sentences have not seen an <EOS> token so far
        # if one <EOS> token was seen the sentence is finished
        has_eos = has_eos | (next_tokens == eos_token_id)
        # either append a padding token here if <EOS> has been seen or append next token
        tokens_to_add = next_tokens.masked_fill(has_eos, eos_token_id)
        all_token_ids = torch.cat([all_token_ids, tokens_to_add.unsqueeze(-1)], dim=-1)

        # update input_ids, attn_mask and position_ids
        input_ids = tokens_to_add.clone().detach().reshape([batch_size, 1]).to(device).to(torch.int32)
        position_ids = (position_ids[:, -1] + 1).reshape(batch_size, 1).to(torch.int32)
        attention_mask = torch.cat([attention_mask, torch.ones([batch_size, 1]).type_as(
            attention_mask)], 1).to(device).to(torch.int32)

        past = []
        if use_onnxruntime:
            for i in range(num_layer):
                past_i = (torch.from_numpy(result[i + 1]) if isinstance(
                    result[i + 1], numpy.ndarray) else result[i + 1].clone().detach())
                past.append(past_i.to(device).to(torch.float32))

            slice_input = get_slice_inputs(input_ids, attention_mask, position_ids, past)
        else:
            try:
                past = result.past_key_values
            except IndexError:
                pass

        if torch.all(has_eos):
            break

    return all_token_ids
