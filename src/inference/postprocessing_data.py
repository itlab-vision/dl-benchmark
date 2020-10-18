import numpy as np


def delete_incorrect_time(time, min_correct_time):
    valid_time = []
    for i in range(len(time)):
        if time[i] >= min_correct_time:
            valid_time.append(time[i])
    return valid_time


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
    time.sort()
    latency = np.median(time)
    return latency


def calculate_fps(pictures, time):
    if time == 0:
        return -1
    return pictures / time
