from diffusers import AutoPipelineForText2Image
import torch

from model_handler import ModelHandler


class KandinskyV21(ModelHandler):
    def set_model_weights(self, **kwargs):
        self.weights = None
        self.pretrained = True
        self.use_custom_compile_step = True

    def create_model(self, precision, **kwargs):
        return AutoPipelineForText2Image.from_pretrained(
            'kandinsky-community/kandinsky-2-1',
            torch_dtype=torch.float16 if precision == 'FP16' else torch.float32,
        )

    def compile_model(self, model, mode, backend, **kwargs):
        model.unet = torch.compile(model.unet, mode=mode, backend=backend, fullgraph=True)
        return model
