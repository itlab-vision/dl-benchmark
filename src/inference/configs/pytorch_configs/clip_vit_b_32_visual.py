from transformers.models.clip import CLIPVisionModelWithProjection

from clip_vit_b_32_text import ClipVitB32Text


class ClipVitB32Visual(ClipVitB32Text):
    def create_model(self, should_be_traced, **kwargs):
        trace_args = self.get_traced_loading_flags() if should_be_traced else {}
        return CLIPVisionModelWithProjection.from_pretrained(self.model_dir, **trace_args)
