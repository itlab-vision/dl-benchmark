from transformers import AutoModelForTokenClassification

from model_handler import ModelHandler


class BertBaseNer(ModelHandler):
    def set_model_weights(self, **kwargs):
        self.weights = None
        self.pretrained = True

    def create_model(self, should_be_traced, **kwargs):
        trace_args = self.get_traced_loading_flags() if should_be_traced else {}
        no_cache_args = self.get_no_cache_flags()
        return AutoModelForTokenClassification.from_pretrained('dslim/bert-base-NER',
                                                               **trace_args, **no_cache_args)
