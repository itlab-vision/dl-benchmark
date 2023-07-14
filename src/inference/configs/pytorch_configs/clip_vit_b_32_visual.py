from transformers.models.clip import CLIPVisionModelWithProjection

from clip_vit_b_32_text import ClipVitB32Text


class ClipVitB32Visual(ClipVitB32Text):
    def create_model(self, **kwargs):
        return CLIPVisionModelWithProjection.from_pretrained(self.model_dir)
