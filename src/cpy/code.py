import board
import time
from adafruit_ble import BLERadio
from adafruit_ble.services.nordic import UARTService
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from ideaboard import IdeaBoard

ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)
ib = IdeaBoard()

print("Starting BLE...")

def stop_motors():
    ib.motor_1.throttle = 0
    ib.motor_2.throttle = 0

def handle_w_down():
    print("W pressed")
    ib.motor_1.throttle = 1
    ib.motor_2.throttle = 1

def handle_w_up():
    print("W released")
    stop_motors()

def handle_a_down():
    print("A pressed")
    ib.motor_1.throttle = 1
    ib.motor_2.throttle = -1

def handle_a_up():
    print("A released")
    stop_motors()

def handle_s_down():
    print("S pressed")
    ib.motor_1.throttle = -1
    ib.motor_2.throttle = -1

def handle_s_up():
    print("S released")
    stop_motors()

def handle_d_down():
    print("D pressed")
    ib.motor_1.throttle = -1
    ib.motor_2.throttle = 1

def handle_d_up():
    print("D released")
    stop_motors()


def handle_command(cmd):
    if cmd == "W_DOWN":
        handle_w_down()
    elif cmd == "W_UP":
        handle_w_up()
    elif cmd == "A_DOWN":
        handle_a_down()
    elif cmd == "A_UP":
        handle_a_up()
    elif cmd == "S_DOWN":
        handle_s_down()
    elif cmd == "S_UP":
        handle_s_up()
    elif cmd == "D_DOWN":
        handle_d_down()
    elif cmd == "D_UP":
        handle_d_up()
    else:
        print("Unknown:", cmd)


while True:
    print("Advertising...")
    ble.start_advertising(advertisement)

    while not ble.connected:
        pass

    print("Connected!")
    ble.stop_advertising()

    while ble.connected:
        if uart.in_waiting:
            data = uart.read(uart.in_waiting).decode("utf-8").strip()
            commands = data.split("\n")

            for cmd in commands:
                if cmd:
                    handle_command(cmd)

    print("Disconnected")
