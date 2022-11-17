import re


def get_param_from_data(data, tag):
    if data is not None:
        return data.get(tag)
    else:
        return None


def get_correct_path(path):
    if path is not None and ' ' in path and '"' not in path:
        path = '"' + path + '"'
    return path


def camel_to_snake(string):
    groups = re.findall('([A-z][a-z0-9]*)', string)
    return '_'.join([i.lower() for i in groups])


def get_typed_from_str(text):
    if text == 'False':
        return False
    if text == 'True':
        return True
    if text.isdigit():
        return int(text)
    if is_number(text):
        return float(text)
    return text or ''


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
