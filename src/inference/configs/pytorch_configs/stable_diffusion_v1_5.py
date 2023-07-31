from diffusers import StableDiffusionPipeline
import torch

from model_handler import ModelHandler


class StableDiffusionV15(ModelHandler):
    def set_model_weights(self, **kwargs):
        self.weights = None
        self.pretrained = True
        self.use_custom_compile_step = True

    def create_model(self, precision, **kwargs):
        return StableDiffusionPipeline.from_pretrained(
            'runwayml/stable-diffusion-v1-5',
            torch_dtype=torch.float16 if precision == 'FP16' else torch.float32,
        )

    def compile_model(self, model, mode, backend, **kwargs):
        model.unet = torch.compile(model.unet, mode=mode, backend=backend, fullgraph=True)
        return model
