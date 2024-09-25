import time
from typing import Callable, Literal
from nguyenpanda.swan import color, yellow


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

    def __enter__(self) -> Callable[[], float]:
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


def __time_consuming(n: int = 5, sleep: float = 0.2):
    for i in range(1, n + 1, 1):
        time.sleep(sleep)
        yield i


@performance(unit='s')
def __a_trivial_function():
    time.sleep(2)
    return 'Hello, World!'


if __name__ == '__main__':
    print(color['m'] + 'Entering `__main__` function' + color.reset)

    with PerformanceTimer(unit='s') as timer:
        for each in __time_consuming():
            print(f'\t {each}. sleep(0.2)')
    print(yellow('Context manager:'), timer())

    print(yellow('Decorator:'), __a_trivial_function())
