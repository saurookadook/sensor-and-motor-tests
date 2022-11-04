#!/usr/bin/env python3

import sys
from inspect import getmembers
from time import sleep

# `hubs` module: https://pybricks.com/ev3-micropython/hubs.html
from ev3dev2 import list_devices
from ev3dev2.button import Button
from ev3dev2.console import Console

# from ev3dev2.led import Leds
from ev3dev2.motor import (
    DcMotor,
    OUTPUT_A,
    OUTPUT_B,
    OUTPUT_C,
    SpeedPercent,
    MoveTank,
)
from ev3dev2.port import LegoPort
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sound import Sound


# from sensor_and_motor_tests import App


def main():
    main_console = Console()
    sound = Sound()
    buttons = Button()

    sound.speak("Welcome to the E V 3 dev project!")

    port_a = LegoPort("outA")
    port_b = LegoPort("outB")
    assert port_a and port_a.status
    assert port_a and port_b.status
    port_a.mode = "dc-motor"
    port_b.mode = "dc-motor"
    sleep(0.5)

    right_motor = DcMotor(port_a.address)
    left_motor = DcMotor(port_b.address)

    # tank_motors = MoveTank(OUTPUT_C, OUTPUT_B, motor_class="ev3dev2.motor.DcMotor")
    front_touch_sensor = TouchSensor(INPUT_1)
    back_touch_sensor = TouchSensor(INPUT_2)

    main_console.text_at("Bootin up . . .", alignment="C")
    sleep(1)
    main_console.text_at("BINGO BANGO!", alignment="C", reset_console=True)
    sound.speak("BINGO BANGO!")

    sleep(1)

    while True:
        if front_touch_sensor.is_pressed:
            right_motor.run_direct(duty_cycle_sp=75)
            left_motor.run_direct(duty_cycle_sp=-75)
            print("Front touch sensor pressed!", file=sys.stderr)
            sound.speak("boop bop beep")

            # tank_motors.on_for_seconds(75, 75, 2)
            sleep(1)
            left_motor.stop()
            right_motor.stop()

        if back_touch_sensor.is_pressed:
            right_motor.run_direct(duty_cycle_sp=-75)
            left_motor.run_direct(duty_cycle_sp=75)
            print("Back touch sensor pressed!", file=sys.stderr)
            sound.speak("beep bop boop")

            # tank_motors.on_for_seconds(75, 75, 2)
            sleep(1)
            left_motor.stop()
            right_motor.stop()

        # sleep(0.01)

        if buttons.buttons_pressed:
            break

    main_console.text_at("I am a pickle!", reset_console=True, alignment="C")
    sound.speak("I am a pickle!")

    main_console.text_at("Bye forever", alignment="C")
    sound.speak("Bye forever")


if __name__ == "__main__":
    main()
