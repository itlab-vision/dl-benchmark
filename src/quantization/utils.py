def get_param_from_data(data, tag):
    if data is not None:
        return data.get(tag)
    else:
        return None


def get_correct_path(path):
    if path is not None and ' ' in path and '"' not in path:
        path = '"' + path + '"'
    return path