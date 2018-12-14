import math
import statistics


def time_to_ms(time):
    for i in range(len(time)):
        time[i] *= 10 ** 3
    return time


def delete_incorrect_time(time, min_correct_time):
    valid_time = []
    for i in range(len(time)):
        if time[i] >= min_correct_time:
            valid_time.append(time[i])
    return valid_time


def three_sigma_rule(time):
    average_time = statistics.mean(time)
    sigm = 0
    for i in range(len(time)):
        sigm += (time[i] - average_time) ** 2
    sigm = math.sqrt(sigm / (len(time) - 1))
    upper_bound = average_time + (3 * sigm)
    lower_bound = average_time - (3 * sigm)
    valid_time = []
    for i in range(len(time)):
        if lower_bound <= time[i] <= upper_bound:
            valid_time.append(time[i])
    return valid_time


def calculate_average_time(time):
    average_time = statistics.mean(time)
    return average_time


def calculate_latency(time):
    time.sort()
    latency = statistics.median(time)
    return latency


def calculate_fps(batch_size, average_time):
    return (batch_size * 1000) / average_time