from diffusers import StableDiffusionPipeline
import torch

from model_handler import ModelHandler


class StableDiffusionV15(ModelHandler):
    def set_model_weights(self, **kwargs):
        self.weights = None
        self.pretrained = True

    def create_model(self, **kwargs):
        return StableDiffusionPipeline.from_pretrained(
            'runwayml/stable-diffusion-v1-5',
            torch_dtype=torch.float32,
        )
