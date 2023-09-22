import sys
import subprocess
from pathlib import Path

from translation.models import load_model
from translation.pipeline import TranslatorPipeline
from translation.vocab import load_vocab

from model_handler import ModelHandler

CONFIG_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(CONFIG_DIR))


class LanguageTranslationTransformer(ModelHandler):
    def set_model_weights(self, **kwargs):
        self.model_dir = CONFIG_DIR.joinpath('pytorch_configs', self.model_name)
        self.vocab = None
        self.encoder = None
        self.decoder = None

        self.pretrained = True
        self.use_custom_compile_step = False

    def download_model_weigths(self, custom_models_links, precision='FP32', device='cpu'):
        subprocess.run(['wget', '-O', str(self.vocab_path), custom_models_links['vocab']])
        subprocess.run(['wget', '-O', str(self.transformer_path), custom_models_links['transformer']])

    def create_model(self, custom_models_links, precision='FP32', device='cpu', **kwargs):
        self.model_files_dir = self.model_dir / 'pytorch' / precision
        self.model_files_dir.mkdir(parents=True, exist_ok=True)
        self.transformer_path = self.model_files_dir / 'transformer.pt'
        self.vocab_path = self.model_files_dir / 'vocab.pt'

        self.download_model_weigths(custom_models_links, precision, device)

        self.vocab = load_vocab(self.vocab_path)
        self.encoder, self.decoder = load_model(self.transformer_path, self.vocab, device=device)

        return TranslatorPipeline(self.vocab, self.encoder, self.decoder)
