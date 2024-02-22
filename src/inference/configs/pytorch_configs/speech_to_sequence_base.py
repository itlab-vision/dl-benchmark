import torch
import torchaudio
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor

from configs.pytorch_configs.model_handler import ModelHandler

MAX_TEXT_LEN = 70  # maximum number of words in output text


class Speech2SequenceBase(ModelHandler):
    def __init__(self, name):
        super().__init__()
        self.set_model_name(name)

    def set_model_weights(self, **kwargs):
        self.weights = None
        self.pretrained = True
        self.use_custom_trace_step = False

    def create_model(self, trust_remote_code=False, **kwargs):
        no_cache_args = self.get_no_cache_flags()

        params = dict(pretrained_model_name_or_path=self.model_name,
                      trust_remote_code=trust_remote_code,
                      **no_cache_args)

        if kwargs['precision'] == 'BF16':
            params.update({'torch_dtype': torch.bfloat16})
        elif kwargs['precision'] == 'FP16':
            params.update({'torch_dtype': torch.float16})

        return AutoModelForSpeechSeq2Seq.from_pretrained(**params)


def create_processor(model, task='transcribe', language='ru'):
    """
    Create AutoProcessor for model_name with optional target language and task.
    :param model: Transformers model instance
    :param language: ru by default
    :param task: transcribe by default
    :returns: AutoProcessor
    """
    params = {'pretrained_model_name_or_path': model.name_or_path, 'task': task, 'language': language}

    processor = AutoProcessor.from_pretrained(**params)
    processor.tokenizer.padding_side = 'left'
    processor.tokenizer.pad_token = processor.tokenizer.eos_token
    model.config.forced_decoder_ids = processor.get_decoder_prompt_ids(language=language, task=task)
    return processor


def process_audio(processor, input_audio, sampling_rate=16000):
    """
    Pre-process audio with its sampling rate by processor.
    Adjusts audio sampling rate by processor sampling rate automatically.
    :param processor: AutoProcessor instance
    :param input_audio: audio waveform
    :param sampling_rate: audio sampling rate
    :returns: dict
    """
    model_sampling_rate = processor.feature_extractor.sampling_rate
    if sampling_rate != processor.feature_extractor.sampling_rate:
        resampler = torchaudio.transforms.Resample(sampling_rate, model_sampling_rate)
        input_audio = resampler(input_audio)
    return processor(input_audio, sampling_rate=model_sampling_rate, return_tensors='pt')


def generate(model, inputs, device, processor):
    input_features = inputs['input_features'].to(device).to(model.dtype)
    return model.generate(
        input_features,
        max_new_tokens=MAX_TEXT_LEN,
        pad_token_id=processor.tokenizer.pad_token_id,
        eos_token_id=processor.tokenizer.eos_token_id,
    )


def decode(processor, outputs):
    decoded_outputs = processor.batch_decode(outputs, skip_special_tokens=True)
    return decoded_outputs
