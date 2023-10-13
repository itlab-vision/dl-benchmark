def create_inference_session(model, provider_with_options, session_options, precision):
    if provider_with_options[0] == 'TensorrtExecutionProvider':
        return create_inference_session_tensorrt_pipeline(precision)
    else:
        return create_inference_session_onnx_pipeline(model, provider_with_options, session_options)


def create_inference_session_onnx_pipeline(model, provider_with_options, session_options):
    from diffusers import OnnxStableDiffusionPipeline
    pipe = OnnxStableDiffusionPipeline.from_pretrained(
        model,
        provider=provider_with_options,
        sess_options=session_options,
    )
    return pipe


def create_inference_session_tensorrt_pipeline(precision, **kwargs):
    import torch

    from diffusers.pipelines.stable_diffusion import StableDiffusionPipelineOutput
    from onnxruntime.transformers.models.stable_diffusion.onnxruntime_tensorrt_txt2img import OnnxruntimeTensorRTStableDiffusionPipeline
    from typing import List, Optional, Union

    model_name_or_path = 'runwayml/stable-diffusion-v1-5'
    revision = 'fp16' if precision == 'FP16' else 'main'
    torch_dtype = torch.float16 if precision == 'FP16' else torch.float32

    class ConfigurableOnnxruntimeTensorRTStableDiffusionPipeline(OnnxruntimeTensorRTStableDiffusionPipeline):
        @torch.no_grad()
        def __call__(
            self,
            prompt: Optional[Union[str, List[str]]] = None,
            num_inference_steps: int = 50,
            guidance_scale: float = 7.5,
            negative_prompt: Optional[Union[str, List[str]]] = None,
            generator: Optional[Union[torch.Generator, List[torch.Generator]]] = None,
        ):
            r"""
            Function invoked when calling the pipeline for generation.

            Args:
                prompt (`str` or `List[str]`, *optional*):
                    The prompt or prompts to guide the image generation. If not defined, one has to pass `prompt_embeds`.
                    instead.
                num_inference_steps (`int`, *optional*, defaults to 50):
                    The number of denoising steps. More denoising steps usually lead to a higher quality image at the
                    expense of slower inference.
                guidance_scale (`float`, *optional*, defaults to 7.5):
                    Guidance scale as defined in [Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598).
                    `guidance_scale` is defined as `w` of equation 2. of [Imagen
                    Paper](https://arxiv.org/pdf/2205.11487.pdf). Guidance scale is enabled by setting `guidance_scale >
                    1`. Higher guidance scale encourages to generate images that are closely linked to the text `prompt`,
                    usually at the expense of lower image quality.
                negative_prompt (`str` or `List[str]`, *optional*):
                    The prompt or prompts not to guide the image generation. If not defined, one has to pass
                    `negative_prompt_embeds`. instead. If not defined, one has to pass `negative_prompt_embeds`. instead.
                    Ignored when not using guidance (i.e., ignored if `guidance_scale` is less than `1`).
                generator (`torch.Generator` or `List[torch.Generator]`, *optional*):
                    One or a list of [torch generator(s)](https://pytorch.org/docs/stable/generated/torch.Generator.html)
                    to make generation deterministic.

            """
            self.generator = generator
            self.denoising_steps = num_inference_steps
            self.guidance_scale = guidance_scale

            # Pre-compute latent input scales and linear multistep coefficients
            self.scheduler.set_timesteps(self.denoising_steps, device=self.torch_device)

            # Define call parameters
            if prompt is not None and isinstance(prompt, str):
                batch_size = 1
                prompt = [prompt]
            elif prompt is not None and isinstance(prompt, list):
                batch_size = len(prompt)
            else:
                raise ValueError(f'Expected prompt to be of type list or str but got {type(prompt)}')

            if negative_prompt is None:
                negative_prompt = [''] * batch_size

            if negative_prompt is not None and isinstance(negative_prompt, str):
                negative_prompt = [negative_prompt]

            assert len(prompt) == len(negative_prompt)

            if batch_size > self.max_batch_size:
                raise ValueError(
                    f'Batch size {len(prompt)} is larger than allowed {self.max_batch_size}. If dynamic shape is used, then maximum batch size is 4',
                )

            self._OnnxruntimeTensorRTStableDiffusionPipeline__allocate_buffers(self.image_height, self.image_width, batch_size)

            with torch.inference_mode(), torch.autocast('cuda'):
                # CLIP text encoder
                text_embeddings = self._OnnxruntimeTensorRTStableDiffusionPipeline__encode_prompt(prompt, negative_prompt)

                # Pre-initialize latents
                num_channels_latents = self.unet.config.in_channels
                latents = self.prepare_latents(
                    batch_size,
                    num_channels_latents,
                    self.image_height,
                    self.image_width,
                    torch.float32,
                    self.torch_device,
                    generator,
                )

                # UNet denoiser
                latents = self._OnnxruntimeTensorRTStableDiffusionPipeline__denoise_latent(latents, text_embeddings)

                # VAE decode latent
                images = self._OnnxruntimeTensorRTStableDiffusionPipeline__decode_latent(latents)

            images, has_nsfw_concept = self.run_safety_checker(images, self.torch_device, torch_dtype)
            images = self.numpy_to_pil(images)
            return StableDiffusionPipelineOutput(images=images, nsfw_content_detected=has_nsfw_concept)

    pipe = ConfigurableOnnxruntimeTensorRTStableDiffusionPipeline.from_pretrained(
        model_name_or_path,
        revision=revision,
        torch_dtype=torch_dtype,
        image_height=512,
        image_width=512,
    )
    pipe.set_cached_folder(model_name_or_path, revision=revision)
    pipe = pipe.to('cuda')

    return pipe
