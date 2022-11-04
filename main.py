#!/usr/bin/env python3

import sys
from inspect import getmembers
from time import sleep

# `hubs` module: https://pybricks.com/ev3-micropython/hubs.html
from sensor_and_motor_tests import EV3App


def main():
    test_app = EV3App(
        name="test app",
    )

    test_app.boot_up_greeting()

    while True:
        if test_app._front_touch_sensor.is_pressed:
            print("Front touch sensor pressed!", file=sys.stderr)
            test_app._sound.speak("boop bop beep")
            test_app.drive(speed=75, direction="backwards")

        if test_app._back_touch_sensor.is_pressed:
            print("Back touch sensor pressed!", file=sys.stderr)
            test_app._sound.speak("beep bop boop")
            test_app.drive(speed=75, direction="forwards")

        # sleep(0.01)

        if test_app._buttons.buttons_pressed:
            break

    test_app.shut_down()


if __name__ == "__main__":
    main()
