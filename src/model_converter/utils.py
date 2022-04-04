import os


def get_all_downloaded_public_models_in_dir(root_dir):
    public_models_dir = os.path.join(root_dir, 'public/')
    models = [f for f in os.listdir(public_models_dir) if os.path.isdir(os.path.join(public_models_dir, f))]
    return models
