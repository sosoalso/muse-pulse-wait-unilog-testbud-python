import threading
import time
from functools import wraps


class pulse:
    def __init__(self, duration, off_method):
        self.duration = duration
        self.off_method = off_method

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            threading.Thread(target=self.pulse_thread).start()
            return result

        return wrapper

    def pulse_thread(self):
        time.sleep(self.duration)
        self.off_method()
        print("Relay is now off")


# @Pulse(5.0, off_callback)  # 5초 후에 relay_off를 호출
# def method():
#     on_callback()
