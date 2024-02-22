import numpy as np


def delete_incorrect_time(time, num_tokens, min_correct_time):
    valid_time = []
    valid_tokens = []
    for i in range(len(time)):
        if time[i] >= min_correct_time:
            valid_time.append(time[i])
            if num_tokens:
                valid_tokens.append(num_tokens[i])
    return valid_time, valid_tokens


def three_sigma_rule(time):
    average_time = np.mean(time)
    sigm = np.std(time)
    upper_bound = average_time + (3 * sigm)
    lower_bound = average_time - (3 * sigm)
    valid_time = []
    for i in range(len(time)):
        if lower_bound <= time[i] <= upper_bound:
            valid_time.append(time[i])
    return valid_time


def calculate_average_time(time):
    average_time = np.mean(time)
    return average_time


def calculate_latency(time):
    """
    Calculate latency and standard deviation from list of times taken for each inference operation
    :param time: list of times taken for each inference operation
    """
    time.sort()
    latency_std = np.std(time)
    latency = np.median(time)
    return latency, latency_std


def calculate_batch_fps(batch_size, time):
    if time == 0:
        return -1
    return batch_size / time


def calculate_average_fps(iter_number, batch_size, inference_time):
    return iter_number * batch_size / inference_time


def calculate_latency_per_value(inference_time, values):
    """
    Calculate latency per <value> (token for text-gen/second for speech2text) list for each iteration
    :param inferency_time: list of times taken for each inference operation
    :param values: list of the number of values (example: tokens generated or length (seconds) of audio processed
                                                 in each inference operation)
    """
    if not values:
        return None
    assert len(inference_time) == len(values), 'Inference time length != values length'
    return list(map(lambda x, y: x / y, inference_time, values))


def calculate_performance_metrics_sync_mode(batch_size, inference_time, min_infer_time=0.0,
                                            num_tokens=None, audios_lengths=None, audio_sampling_rate=None):
    first_inference_time = inference_time[0]
    iterations_num = len(inference_time)
    execution_time = sum(inference_time)
    latency_per_token_median = None
    latencies_per_second_median = None
    average_audio_length = None

    inference_time, num_tokens = delete_incorrect_time(inference_time, num_tokens, min_infer_time)
    if num_tokens:
        latencies_per_token = calculate_latency_per_value(inference_time, num_tokens)
        latencies_per_token = three_sigma_rule(latencies_per_token)
        latency_per_token_median = np.median(latencies_per_token)
    if audios_lengths:
        latencies_per_second = calculate_latency_per_value(inference_time, audios_lengths)
        latencies_per_second = three_sigma_rule(latencies_per_second)
        latencies_per_second_median = np.median(latencies_per_second)
        average_audio_length = calculate_average_time(three_sigma_rule(audios_lengths))

    inference_time = three_sigma_rule(inference_time)
    average_time = calculate_average_time(inference_time)
    latency, latency_std = calculate_latency(inference_time)
    batch_fps = calculate_batch_fps(batch_size, latency)
    average_fps = calculate_average_fps(iterations_num, batch_size, sum(inference_time))

    inference_result = {
        'iterations_num': iterations_num,
        'execution_time': round(execution_time, 3),
        'first_inference_time': round(first_inference_time, 5),
        'latency_avg': round(average_time, 5),
        'latency_median': round(latency, 5),
        'latency_std': round(latency_std, 5),
        'latency_max': round(max(inference_time), 5),
        'latency_min': round(min(inference_time), 5),
        'latency_per_token': round(latency_per_token_median, 5) if latency_per_token_median is not None else None,
        'num_tokens': np.median(num_tokens) if num_tokens else None,
        'min_num_tokens': min(num_tokens) if num_tokens else None,
        'max_num_tokens': max(num_tokens) if num_tokens else None,
        'audio_len_avg': round(average_audio_length, 3) if average_audio_length else None,
        'audio_sampling_rate': audio_sampling_rate,
        'latency_per_second': round(latencies_per_second_median,
                                    5) if latencies_per_second_median is not None else None,
        'batch_throughput': round(batch_fps, 3),
        'throughput': round(average_fps, 3),
    }
    return inference_result


def log_performance_metrics_sync_mode(log, average_time, fps, latency):
    log.info(f'Average time of single pass : {average_time:.3f}')
    log.info(f'FPS : {fps:.3f}')
    log.info(f'Latency : {latency:.3f}')


def print_performance_metrics_sync_mode(log, average_time, fps, latency):
    log.info(f'{average_time:.3f},{fps:.3f},{latency:.3f}')


def calculate_performance_metrics_async_mode(inference_time, batch_size, iteration_count):
    average_time = inference_time / iteration_count
    fps = calculate_average_fps(iteration_count, batch_size, inference_time)
    inference_result = {
        'execution_time': round(inference_time, 3),
        'latency_avg': round(average_time, 5),
        'throughput': round(fps, 3),
    }
    return inference_result


def log_performance_metrics_async_mode(log, average_time, fps):
    log.info('Average time of single pass : {0:.3f}'.format(average_time))
    log.info('FPS : {0:.3f}'.format(fps))


def print_performance_metrics_async_mode(average_time, fps):
    print('{0:.3f},{1:.3f}'.format(average_time, fps))
