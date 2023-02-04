#!/usr/bin/env python3

# import sys
# from inspect import getmembers
# from time import sleep, time

# from ev3dev2.motor import LargeMotor, MediumMotor
from ev3dev2.port import LegoPort

# `hubs` module: https://pybricks.com/ev3-micropython/hubs.html
from sensor_and_motor_tests.ev3apps import EV3App_Basically_A_Car, EV3Tank, EV3TachoTank


def main():
    # basically_a_car = EV3App_Basically_A_Car(
    #     name="basically_a_car",
    #     port_a=LegoPort("outA"),
    #     port_b=LegoPort("outB"),
    #     port_d=LegoPort("outD"),
    #     # disable_sound=True,
    # )

    # # basically_a_car.boot_up_greeting()

    # basically_a_car.run()

    tank_app = EV3Tank(
        name="basically_a_tank",
        port_a=LegoPort("outA"),
        port_b=LegoPort("outB"),
        # port_d=LegoPort("outD"),
        # disable_sound=True,
    )

    tank_app.run()


if __name__ == "__main__":
    main()
