from enum import Enum


class Status(Enum):
    EXIT_SUCCESS = 0
    EXIT_FAILURE = 1

    INFERENCE_FAILURE = 2
    CPP_BENCHMARK_FAILURE = 3
    INFERENCE_EXCEPTION = 4

    PROCESS_TIMEOUT = -9
    PROCESS_CREATE_ERROR = 127
    INFERENCE_SEGMENTATION_FAULT = 139
    PROCESS_CMD_ERROR = 400
    EXECUTOR_NOT_FOUND = 438

    @classmethod
    def has_key(cls, name):
        return name in cls.__members__

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
