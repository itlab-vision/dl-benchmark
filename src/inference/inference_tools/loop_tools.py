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

            print(f'start inference max {iter_count} iterations or {test_duration} seconds')

            while (iteration <= iter_count) or (infer_duration < test_duration and test_duration > 0):
                print('.', end='')
                infer_res = inference_func(*args, **kwargs)
                if isinstance(infer_res, tuple):
                    exec_time, iter_tokens = infer_res
                    if exec_time > 0:
                        num_tokens.append(iter_tokens)
                else:
                    exec_time = infer_res
                if exec_time > 0:
                    time_infer.append(exec_time)
                infer_duration = sum(time_infer)
                iteration += 1
            print('')

            return time_infer, num_tokens

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
