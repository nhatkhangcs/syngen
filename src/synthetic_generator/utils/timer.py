import time
from typing import Callable, Literal


class PerformanceTimer:
    """
    A context manager and utility class for measuring the performance time
    of code execution in seconds (s), milliseconds (ms), or nanoseconds (ns).

    Attributes:
        unit (str): The unit of time to measure, either 's' (seconds),
                    'ms' (milliseconds), or 'ns' (nanoseconds).
        timer (Callable[[], float]): The appropriate time measurement function
                                     depending on the unit.
        result (float): The elapsed time measured after execution.
    """

    def __init__(self, unit: Literal['s', 'ms', 'ns'] = 'ms'):
        """
        Initialize the PerformanceTimer with the specified unit of measurement.

        Args:
            unit (Literal['s', 'ms', 'ns']): The time unit to measure in.
                                             Defaults to 'ms' (milliseconds).
        """
        self.unit: Literal['s', 'ms', 'ns'] = unit
        self.timer: Callable[[], float]
        self.result = -1

        if self.unit == 'ns':
            self.timer = time.perf_counter_ns
        elif self.unit == 's' or self.unit == 'ms':
            self.timer = time.perf_counter
        else:
            raise NotImplementedError('')

    def __enter__(self) -> 'PerformanceTimer':
        """
        Enters the context manager, starts the timer, and returns the instance.

        Returns:
            Self: The current instance of the PerformanceTimer.
        """
        self.start = self.timer()
        return self

    def __call__(self, unit=None) -> float:
        """
        Allows the PerformanceTimer instance to be called as a function to
        retrieve the recorded elapsed time.

        Returns:
            float: The elapsed time in the original unit of the timer.
        """
        return self.to(unit if unit else self.unit)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the context manager, stops the timer, and computes the result.

        Args:
            exc_type: The exception type (if any) raised inside the block.
            exc_val: The exception value (if any) raised inside the block.
            exc_tb: The traceback object (if any) raised inside the block.
        """
        self.end = self.timer()
        self.result = self.end - self.start
        if self.unit == 'ms':
            self.result *= 1e3

    def to(self, unit: Literal['s', 'ms', 'ns'] = 'ms') -> float:
        """
        Converts the recorded time to the specified unit of measurement.

        Args:
            unit (Literal['s', 'ms', 'ns']): The desired unit of time.

        Returns:
            float: The recorded time in the specified unit.

        Raises:
            NotImplementedError: If the conversion between units is unsupported.
        """
        result = self.result

        if unit == self.unit:
            return result

        if unit == 's':
            if self.unit == 'ms':
                return result * 1e-3
            elif self.unit == 'ns':
                return result * 1e-9
        elif unit == 'ms':
            if self.unit == 's':
                return result * 1e3
            elif self.unit == 'ns':
                return result * 1e-6
        elif unit == 'ns':
            if self.unit == 's':
                return result * 1e9
            elif self.unit == 'ms':
                return result * 1e6

        raise NotImplementedError(f'Unsupported conversion from {self.unit} to {unit}')


def performance(unit: Literal['s', 'ms', 'ns'] = 'ms'):
    """
    A decorator that measures the performance time of a function and returns
    both the function's return value and the elapsed time.

    Args:
        unit (Literal['s', 'ms', 'ns']): The unit of time to measure in.
                                         Defaults to 'ms' (milliseconds).

    Returns:
        Callable: A decorated function that will return a tuple containing
                  the elapsed time and the original return value of the function.
    """

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
    print('Entering `__main__` function')

    with PerformanceTimer(unit='s') as _timer:
        for each in __time_consuming():
            print(f'\t {each}. sleep(0.2)')
    print('Context manager (s) :', _timer())
    print('Context manager (ms):', _timer('ms'))
    print('Context manager (ns):', _timer.to('ns'))

    print('Decorator:', __a_trivial_function())
