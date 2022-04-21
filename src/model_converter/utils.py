import os
import shutil
from pathlib import Path


def get_all_downloaded_public_models_in_dir(root_dir):
    public_models_dir = os.path.join(root_dir, 'public/')
    models = [f for f in os.listdir(public_models_dir) if os.path.isdir(os.path.join(public_models_dir, f))]
    return models


def copy_converted_model_files(src_dir, dst_dir):
    Path(dst_dir).mkdir(parents=True, exist_ok=True)
    src_files_list = [os.path.join(src_dir, f) for f in os.listdir(src_dir)
                      if f.endswith(('.xml', '.bin'))]
    for src_file in src_files_list:
        shutil.copy(src_file, dst_dir)
