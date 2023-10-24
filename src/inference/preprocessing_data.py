import ast
import re


def names_arg(values):
    if values is not None:
        values = values.split(',')

    return values


def parse_input_arg(values, input_names):
    return_values = {}
    if values is not None:
        matches = re.findall(r'(.*?)\[(.*?)\],?', values)
        if matches:
            for i, match in enumerate(matches):
                name, value = match
                value = ast.literal_eval(value)
                if name != '':
                    return_values[name] = value
                else:
                    if input_names is None:
                        raise ValueError('Please set --input-names parameter'
                                         f' or use input0[value0],input1[value1] format instead {values}')
                    return_values[input_names[i]] = list(value)
        else:
            raise ValueError(f'Unable to parse input parameter: {values}')
    return return_values


def parse_layout_arg(values, input_names):
    return_values = {}
    if values is not None:
        matches = re.findall(r'(.*?)\((.*?)\),?', values)
        if matches:
            for i, match in enumerate(matches):
                name, value = match
                if name != '':
                    return_values[name] = value
                else:
                    if input_names is None:
                        raise ValueError(f'Please set --input-names parameter'
                                         f' or use input0(value0),input1(value1) format instead {values}')
                    return_values[input_names[i]] = value
        else:
            values = values.split(',')
            return_values = dict(zip(input_names, values))
    return return_values


def create_dict_for_transformer(args, default_layout='NCHW'):
    dictionary = {}
    for name in args.input_names or []:
        if 'channel_swap' in args:
            channel_swap = args.channel_swap.get(name, None)
        else:
            channel_swap = None
        mean = args.mean.get(name, None)
        input_scale = args.input_scale.get(name, None)
        layout = args.layout.get(name, default_layout)
        dictionary[name] = {'channel_swap': channel_swap, 'mean': mean,
                            'input_scale': input_scale, 'layout': layout}

    return dictionary
