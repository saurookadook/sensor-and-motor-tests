#!/usr/bin/env python3

import sys
from inspect import getmembers
from time import sleep, time

from ev3dev2.motor import LargeMotor, MediumMotor
from ev3dev2.port import LegoPort

# `hubs` module: https://pybricks.com/ev3-micropython/hubs.html
from sensor_and_motor_tests import EV3App, EV3App_Basically_A_Car


def main():
    basically_a_car = EV3App_Basically_A_Car(
        name="basically_a_car",
        port_a=LegoPort("outA"),
        port_b=LegoPort("outB"),
        port_d=LegoPort("outD"),
        disable_sound=True,
    )

    basically_a_car.boot_up_greeting()

    basically_a_car.run()


# def main():
#     test_app = EV3App(
#         name="test app",
#         disable_sound=True
#     )

#     test_app.boot_up_greeting()

#     start_time = time()
#     # main_timer = time()
#     latest_direction = "forwards"
#     while True:
#         test_app.drive(speed=50, direction=latest_direction, duration=-1)

#         if test_app._front_touch_sensor.is_pressed:
#             test_app.stop()
#             latest_direction = "backwards"
#             print("Front touch sensor pressed!", file=sys.stderr)
#             test_app.say("Ouch, my face!")
#             test_app.drive(speed=75, direction=latest_direction, duration=-1)
#             test_app.say("boop bop beep")

#         elif test_app._back_touch_sensor.is_pressed:
#             test_app.stop()
#             latest_direction = "forwards"
#             print("Back touch sensor pressed!", file=sys.stderr)
#             test_app.say("Ouch, my butthole!")
#             test_app.drive(speed=75, direction=latest_direction, duration=-1)
#             test_app.say("beep bop boop")

#         # sleep(0.01)

#         if test_app._buttons.buttons_pressed or time() - start_time >= 10000:
#             test_app.stop()
#             break

#     test_app.shut_down()


if __name__ == "__main__":
    main()
