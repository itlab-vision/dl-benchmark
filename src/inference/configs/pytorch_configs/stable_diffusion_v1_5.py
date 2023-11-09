from diffusers import StableDiffusionPipeline
from diffusers.models.unet_2d_condition import UNet2DConditionOutput

import torch

from model_handler import ModelHandler


class StableDiffusionV15(ModelHandler):
    def set_model_weights(self, **kwargs):
        self.weights = None
        self.pretrained = True
        self.use_custom_compile_step = True
        self.use_custom_trace_step = True

    def create_model(self, precision, **kwargs):
        return StableDiffusionPipeline.from_pretrained(
            'runwayml/stable-diffusion-v1-5',
            torch_dtype=torch.float16 if precision == 'FP16' else torch.float32,
        )

    def compile_model(self, model, mode, backend, **kwargs):
        model.unet = torch.compile(model.unet, mode=mode, backend=backend, fullgraph=True)
        return model

    def generate_inputs(self, device):
        sample = torch.randn(2, 4, 64, 64).to(device)
        timestep = torch.rand(1).to(device) * 999
        encoder_hidden_states = torch.randn(2, 77, 768).to(device)
        return sample, timestep, encoder_hidden_states

    def trace_model(self, model, device, **kwargs):
        import functools

        unet = model.unet
        unet.eval()
        unet.to(memory_format=torch.channels_last)
        unet.forward = functools.partial(unet.forward, return_dict=False)

        inputs = self.generate_inputs(device)

        unet_traced = torch.jit.trace(unet, inputs)
        unet_traced.eval()

        class TracedUNet(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self.in_channels = model.unet.in_channels
                self.device = model.unet.device
                self.config = model.unet.config

            def forward(self, latent_model_input, t, encoder_hidden_states, **kwargs):
                sample = unet_traced(latent_model_input, t, encoder_hidden_states)[0]
                return UNet2DConditionOutput(sample=sample)

        model.unet = TracedUNet()

        return model
