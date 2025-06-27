import threading
from time import sleep

class ServiceManager:
    def __init__(self, gpio_controller):
        self.gpio_controller = gpio_controller
        self.running = False
        self.thread = None

    def start_distance_monitor(self, callback, interval=1.0):
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, args=(callback, interval))
        self.thread.start()

    def _monitor_loop(self, callback, interval):
        while self.running:
            distance = self.gpio_controller.measure_distance()
            callback(distance)
            sleep(interval)

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
