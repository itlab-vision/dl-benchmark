import statistics

def delete_incorrect_time(time, min_correct_time):
    valid_time = []
    for i in range(len(time)):
        if time[i] >= min_correct_time:
            valid_time.append(time[i])
    return time

def three_sigma_rule(time):
    average_time = statistics.mean(time)
    sigm = 0
    for i in range(len(time)):
        sigm += (time[i] - average_time) ** 2
    sigm /= len(time) - 1
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

def calculate_fps(average_time):
    average_time *= 10 ** 3
    return 1000 / average_time