import os
import yaml


def make_string_of_one_shape_with_new_batch(original_shape, new_batch):
    dims = original_shape[1:]
    res = f'[{new_batch}'
    for dim in dims:
        res += f',{dim}'
    res += ']'
    return res


def prepare_input_shape_line_with_new_batch(original_shapes, new_batch):
    res = '--input_shape='
    for placeholder in original_shapes:
        shape_as_list = placeholder['shape']
        res += make_string_of_one_shape_with_new_batch(shape_as_list, new_batch)
        res += ','
    res = res[:-1]
    return res


def get_new_input_shape_by_model_name(root_dir, model_name, new_batch):
    yaml_name = os.path.join(root_dir, f'public/{model_name}/model.yml')
    with open(yaml_name, 'r') as stream:
        data_loaded = yaml.safe_load(stream)
        result_input_shape = prepare_input_shape_line_with_new_batch(
            data_loaded['input_info'], new_batch)
    return result_input_shape
