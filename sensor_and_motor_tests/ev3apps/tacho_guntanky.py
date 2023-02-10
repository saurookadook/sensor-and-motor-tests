from inspect import getmembers
from pprint import pprint as pretty_print
from time import sleep, time

from ev3dev2.button import Button
from ev3dev2.console import Console
from ev3dev2.motor import (
    MediumMotor,
)  # possible bug with missing setter for `duty_cycle`
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sound import Sound

from ..app import App
from ..constants import DriveDirection, TurnDirection
from ..utils import debug_logger, safe_init_port


class AbstractEV3Tank(App):

    __slots__ = [
        "_buttons",
        "_console",
        "_sound",
        "_left_motor",
        "_right_motor",
        "_front_touch_sensor",
        "_back_touch_sensor",
        "_current_direction",
        "_drive_direction",
        "_turn_direction",
        "_cruise_speed",
        "_reorient_speed",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.current_direction = DriveDirection.FORWARDS.value
        self.drive_direction = DriveDirection.FORWARDS.value
        self.turn_direction = TurnDirection.STRAIGHT.value
        self.cruise_speed = 80
        self.reorient_speed = 60

    @property
    def buttons(self):
        return self._buttons

    @buttons.setter
    def buttons(self, value):
        self._buttons = value

    @property
    def console(self):
        return self._console

    @console.setter
    def console(self, value):
        self._console = value

    @property
    def sound(self):
        return self._sound

    @sound.setter
    def sound(self, value):
        self._sound = value

    @property
    def left_motor(self):
        return self._left_motor

    @left_motor.setter
    def left_motor(self, value):
        self._left_motor = value

    @property
    def right_motor(self):
        return self._right_motor

    @right_motor.setter
    def right_motor(self, value):
        self._right_motor = value

    @property
    def front_touch_sensor(self):
        return self._front_touch_sensor

    @front_touch_sensor.setter
    def front_touch_sensor(self, value):
        self._front_touch_sensor = value

    @property
    def back_touch_sensor(self):
        return self._back_touch_sensor

    @back_touch_sensor.setter
    def back_touch_sensor(self, value):
        self._back_touch_sensor = value

    @property
    def current_direction(self):
        return self._current_direction

    @current_direction.setter
    def current_direction(self, value):
        try:
            self._current_direction = DriveDirection(value).value
        except ValueError as ve:
            debug_logger(ve)
            # raise ve

    @property
    def drive_direction(self):
        return self._drive_direction

    @drive_direction.setter
    def drive_direction(self, value):
        try:
            self._drive_direction = DriveDirection(value).value
        except ValueError as ve:
            debug_logger(ve)
            # raise ve

    @property
    def turn_direction(self):
        return self._turn_direction

    @turn_direction.setter
    def turn_direction(self, value):
        try:
            self._turn_direction = TurnDirection(value).value
        except ValueError as ve:
            debug_logger(ve)
            # raise ve

    @property
    def cruise_speed(self):
        return self._cruise_speed

    @cruise_speed.setter
    def cruise_speed(self, value):
        self._cruise_speed = value

    @property
    def reorient_speed(self):
        return self._reorient_speed

    @reorient_speed.setter
    def reorient_speed(self, value):
        self._reorient_speed = value

    def _configure_ports_with_mode(self, port_a=None, port_b=None):
        super()._configure_ports_with_mode(self, port_a=port_a, port_b=port_b)


class EV3TachoTank(App):

    __slots__ = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.buttons = Button()
        self.console = Console()
        self.sound = Sound()

        super()._configure_ports_with_mode(
            self, port_a=safe_init_port("a", kwargs), port_b=safe_init_port("b", kwargs)
        )

        self.right_motor = MediumMotor(self._port_a.address)
        self.left_motor = MediumMotor(self._port_b.address)

        self.front_touch_sensor = TouchSensor(INPUT_1)
        self.back_touch_sensor = TouchSensor(INPUT_2)

    def boot_up_greeting(self):
        self.say("Bootin up, baby")
        self._console.text_at("Bootin up . . .", alignment="C")
        sleep(1)
        self._console.text_at("BINGO BANGO!", alignment="C", reset_console=True)
        self.say("BINGO BANGO!")

    def shut_down(self):
        self._console.text_at("I am a pickle!", reset_console=True, alignment="C")
        self.say("I am a pickle!")
        sleep(1)
        self._console.text_at("Bye forever", alignment="C")
        self.say("Bye forever")

    def say(self, text, **kwargs):
        if not self.is_silenced:
            self._sound.speak(text, **kwargs)

    def run(
        self,
    ):
        self.boot_up_greeting()

        current_drive_direction = DriveDirection.FORWARDS.value
        start_time = int(time())

        while True:

            if self.turn_direction != TurnDirection.STRAIGHT.value:
                self.turn_in_drive_direction(
                    turn_direction=TurnDirection.STRAIGHT.value
                )
            self.drive(
                speed=self.cruise_speed,
                drive_direction=current_drive_direction,
                duration=-1,
            )

            if self.front_touch_sensor.is_pressed:
                self.stop()
                current_drive_direction = DriveDirection.REVERSE.value
                turn_direction = self._choose_turn_direction(
                    drive_direction=current_drive_direction,
                    last_turn_direction=self.turn_direction,
                )
                debug_logger(
                    "Front touch sensor pressed!\n",
                    "turn_direction: {}\ndrive_direction: {}\ncurrent_drive_direction: {}".format(
                        turn_direction, self.drive_direction, current_drive_direction
                    ),
                )
                self.say("Ouch, my face!")
                self.turn_in_drive_direction(
                    drive_direction=current_drive_direction,
                    turn_direction=turn_direction,
                )
                self.drive(
                    speed=self.reorient_speed,
                    drive_direction=current_drive_direction,
                    duration=2,
                )
                self.say("boop bop beep")

            elif self._back_touch_sensor.is_pressed:
                self.stop()
                current_drive_direction = DriveDirection.FORWARDS.value
                turn_direction = self._choose_turn_direction(
                    drive_direction=current_drive_direction,
                    last_turn_direction=self.turn_direction,
                )
                debug_logger(
                    "Back touch sensor pressed!\n",
                    "turn_direction: {}\ndrive_direction: {}\ncurrent_drive_direction: {}".format(
                        turn_direction, self.drive_direction, current_drive_direction
                    ),
                )
                self.say("Ouch, my butthole!")
                self.turn_in_drive_direction(
                    drive_direction=current_drive_direction,
                    turn_direction=turn_direction,
                )
                self.drive(
                    speed=self.reorient_speed,
                    drive_direction=current_drive_direction,
                    duration=2,
                )
                self.say("beep bop boop")

            # sleep(0.01)

            if self._buttons.buttons_pressed or time() - start_time >= 300:
                debug_logger(int(time() - start_time))
                self.stop()
                break

        self.shut_down()

    def drive(
        self,
        speed=None,
        left_wheel_speed=None,
        right_wheel_speed=None,
        drive_direction="forwards",
        duration=-1,
    ):
        if drive_direction != self.current_direction:
            self.current_direction = drive_direction

        if speed and not left_wheel_speed:
            # left_wheel_speed = -speed if drive_direction == "forwards" else speed
            left_wheel_speed = speed if drive_direction == "forwards" else -speed
        if speed and not right_wheel_speed:
            # right_wheel_speed = speed if drive_direction == "forwards" else -speed
            right_wheel_speed = -speed if drive_direction == "forwards" else speed

        # self._left_motor.run_direct(duty_cycle_sp=left_wheel_speed)
        # self._right_motor.run_direct(duty_cycle_sp=right_wheel_speed)
        self._base_run_direct(
            left_wheel_speed=left_wheel_speed, right_wheel_speed=right_wheel_speed
        )

        if int(duration) > 0:
            sleep(duration)
            self.stop()

    def forward(self, left_wheel_speed=0, right_wheel_speed=0):
        self._left_motor.run_direct(duty_cycle_sp=left_wheel_speed)
        self._right_motor.run_direct(duty_cycle_sp=-right_wheel_speed)

    def reverse(self, left_wheel_speed=0, right_wheel_speed=0):
        self._left_motor.run_direct(duty_cycle_sp=-left_wheel_speed)
        self._right_motor.run_direct(duty_cycle_sp=right_wheel_speed)

    def _base_run_direct(self, left_wheel_speed=0, right_wheel_speed=0):
        self._left_motor.run_direct(duty_cycle_sp=left_wheel_speed)
        self._right_motor.run_direct(duty_cycle_sp=right_wheel_speed)

    def turn_in_drive_direction(self, drive_direction, turn_direction):
        if turn_direction == self.turn_direction:
            return

        # self.turn_direction = turn_direction
        left_wheel_speed, right_wheel_speed = self._get_base_wheel_speeds_for_turn(
            drive_direction=drive_direction, turn_direction=turn_direction
        )

        if drive_direction == DriveDirection.FORWARDS.value:
            self._base_run_direct(
                left_wheel_speed=left_wheel_speed, right_wheel_speed=-right_wheel_speed
            )
        else:
            self._base_run_direct(
                left_wheel_speed=-left_wheel_speed, right_wheel_speed=right_wheel_speed
            )

        # if turn_direction == "straight":
        #     debug_logger("Straightenin' out!")
        #     self.set_motor_speeds_for_turn(
        #         left_wheel_speed=left_wheel_speed, right_wheel_speed=right_wheel_speed
        #     )
        # elif turn_direction == "left":
        #     debug_logger("Turnin' left!")
        #     self.set_motor_speeds_for_turn(
        #         left_wheel_speed=left_wheel_speed, right_wheel_speed=right_wheel_speed
        #     )
        # elif turn_direction == "right":
        #     debug_logger("Turnin' right!")
        #     self.set_motor_speeds_for_turn(
        #         left_wheel_speed=left_wheel_speed, right_wheel_speed=right_wheel_speed
        #     )

    def set_motor_speeds_for_turn(self, *, left_wheel_speed=0, right_wheel_speed=0):
        self._left_motor.run_direct(left_wheel_speed)
        self._right_motor.run_direct(right_wheel_speed)

    def _choose_turn_direction(self, drive_direction, last_turn_direction):
        if drive_direction == "forward":
            return "right" if last_turn_direction == "left" else "left"
        else:
            return "left" if last_turn_direction == "right" else "right"

    def _get_base_wheel_speeds_for_turn(self, drive_direction, turn_direction):
        left_wheel_speed = 0
        right_wheel_speed = 0

        outer_wheel_speed = self.cruise_speed + 15
        inner_wheel_speed = self.cruise_speed - 15

        if drive_direction == DriveDirection.REVERSE.value:
            left_wheel_speed = (
                outer_wheel_speed
                if turn_direction == TurnDirection.LEFT.value
                else inner_wheel_speed
            )
            right_wheel_speed = (
                inner_wheel_speed
                if turn_direction == TurnDirection.RIGHT.value
                else outer_wheel_speed
            )
        else:
            left_wheel_speed = (
                inner_wheel_speed
                if turn_direction == TurnDirection.LEFT.value
                else outer_wheel_speed
            )
            right_wheel_speed = (
                outer_wheel_speed
                if turn_direction == TurnDirection.RIGHT.value
                else inner_wheel_speed
            )

        return (left_wheel_speed, right_wheel_speed)

    def stop(self):
        self._left_motor.stop()
        self._right_motor.stop()
