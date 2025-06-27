import serial
from time import sleep

class GSMController:
    def __init__(self, port="/dev/ttyAMA0", baudrate=9600):
        self.serial = serial.Serial(port=port, baudrate=baudrate, timeout=1)

    def send_sms(self, number, message):
        self.serial.write(b'AT\r')
        self.serial.write(b'AT+CMGF=1\r')
        sleep(0.5)
        self.serial.write(f'AT+CMGS="{number}"\r'.encode())
        sleep(0.5)
        self.serial.write(f"{message}\x1A".encode())

    def make_call(self, number):
        self.serial.write(b'AT\r')
        sleep(0.2)
        self.serial.write(f'ATD{number};\r'.encode())
