import time
from typing import Callable, Literal


class PerformanceTimer:

    def __init__(self, unit: Literal['s', 'ms', 'ns'] = 'ms'):
        self.unit: str = unit
        self.timer: Callable[[], float]
        self.result = -1

        if self.unit == 'ns':
            self.timer = time.perf_counter_ns
        elif self.unit == 's' or self.unit == 'ms':
            self.timer = time.perf_counter
        else:
            raise NotImplementedError('')

    def __enter__(self):
        self.start = self.timer()
        return lambda: self.result

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = self.timer()
        self.result = self.end - self.start
        if self.unit == 'ms':
            self.result *= 1e3


def performance(unit: Literal['s', 'ms', 'ns'] = 'ms'):
    def wrapper_1(func: Callable):
        def wrapper_2():
            with PerformanceTimer(unit) as timer:
                return_value = func()
            return timer(), return_value

        return wrapper_2

    return wrapper_1


if __name__ == '__main__':
    @performance(unit='ms')
    def __a_trivial_function():
        time.sleep(2)
        return 'Hello, World!'


    print(__a_trivial_function())
