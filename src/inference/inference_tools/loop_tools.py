from functools import wraps
from time import time


def loop_inference(iter_count, test_duration):
    def deco_loop_inference(inference_func):
        @wraps(inference_func)
        def f_loop_inference(*args, **kwargs):
            infer_duration = 0
            iteration = 1
            time_infer = []
            num_tokens = []
            audios_lengths = []
            audio_sampling_rate = None

            print(f'start inference max {iter_count} iterations or {test_duration} seconds')

            while (iteration <= iter_count) or (infer_duration < test_duration and test_duration > 0):
                print('.', end='')
                infer_res = inference_func(*args, **kwargs)
                if isinstance(infer_res, dict):
                    audio_length = None
                    exec_time = infer_res.get('exec_time')
                    iter_tokens = infer_res.get('iter_tokens')
                    audio_length = infer_res.get('audio_length')
                    audio_sampling_rate = infer_res.get('audio_sampling_rate')

                    if exec_time > 0:
                        # save only valid results
                        if iter_tokens is not None:
                            if isinstance(iter_tokens, list):
                                # for batch > 1
                                num_tokens.append(sum(iter_tokens))
                            else:
                                num_tokens.append(iter_tokens)
                        if audio_length is not None:
                            audios_lengths.append(audio_length)
                else:
                    exec_time = infer_res
                if exec_time > 0:
                    time_infer.append(exec_time)
                infer_duration = sum(time_infer)
                iteration += 1
            print('')

            return {'time_infer': time_infer,
                    'num_tokens': num_tokens,
                    'audios_lengths': audios_lengths,
                    'audio_sampling_rate': audio_sampling_rate}

        return f_loop_inference

    return deco_loop_inference


def get_exec_time():
    def deco_get_exec_time(func):
        @wraps(func)
        def f_get_exec_time(*args, **kwargs):
            t0 = time()
            res = func(*args, **kwargs)
            t1 = time()
            exec_time = t1 - t0
            return res, exec_time

        return f_get_exec_time

    return deco_get_exec_time
