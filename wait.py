# ---------------------------------------------------------------------------- #
import threading
import time

# ---------------------------------------------------------------------------- #
import sched_mod


# ---------------------------------------------------------------------------- #
class wait:
    def __init__(self, name, allow_multiple_execution=False):
        self.name = name
        self.scheduler = sched_mod.scheduler(time.time, time.sleep)
        self.count = None
        self.running = False
        self.allow_multiple_execution = allow_multiple_execution

    def wait(self, delay_second, callback, *argument, **kwargs):
        if not self.running or self.allow_multiple_execution:
            self.scheduler.enter(delay_second, 1, callback, argument, kwargs)
            print(f"WAIT '{self.name}' | {delay_second=}\t| callback={callback.__name__}\t| {argument=} {kwargs=}")

    def get_queue(self):
        return self.scheduler.queue

    def get_item(self, id):
        print(f"get Queue: {self.scheduler.queue[id]}")
        return self.scheduler.queue[id]

    def run(self):
        self.running = True
        threading.Thread(target=self._run_scheduler).start()

    def _run_scheduler(self):
        while self.running and not self.scheduler.empty():
            status = self.scheduler.run(blocking=False)
            time.sleep(0.1)
        self.running = False
        print(f"WAIT '{self.name}' stopped")

    def stop(self):
        self.running = False
        print(f"WAIT '{self.name}' stopped forcedly")


def my_print():
    print("my_print() called")


# ---------------------------------------------------------------------------- #
