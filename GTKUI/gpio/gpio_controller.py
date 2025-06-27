from gpiozero import DistanceSensor, OutputDevice
from time import sleep

class GPIOController:
    def __init__(self):
        self.sensor = DistanceSensor(echo=24, trigger=23, max_distance=2.0)
        self.mosfet = OutputDevice(25)

    def measure_distance(self):
        sleep(0.1)
        return round(self.sensor.distance * 100, 2)

    def mosfet_on(self):
        self.mosfet.on()

    def mosfet_off(self):
        self.mosfet.off()
