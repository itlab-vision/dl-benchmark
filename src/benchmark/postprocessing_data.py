import statistics

def delete_incorrect_time(time, min_correct_time):
    for i in range(len(time)):
        if time[i] < min_correct_time:
            time.pop(i)
    return time

def calculate_average_time(time):
    average_time = statistics.mean(time)
    return average_time
    
def calculate_latency(time):
    time.sort()
    latency = statistics.median(time)
    return latency

def calculate_fps(average_time):
    return 1000 / average_time