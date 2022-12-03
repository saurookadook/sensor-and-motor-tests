import sys
from inspect import getmembers
from pprint import pprint as pretty_print
from time import sleep, time

from ev3dev2.button import Button
from ev3dev2.console import Console
from ev3dev2.motor import DcMotor, LargeMotor, MediumMotor, SpeedDPS
from ev3dev2.port import LegoPort
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sound import Sound

from .constants import DriveDirection, TurnDirection


class App:
    _brick_device = None
    _console = None
    _port_a = None
    _port_b = None
    _console = None
    _buttons = None
    _sound = None

    def __init__(self, name="", brick_device=None, **kwargs):
        self.name = name

        self._brick_device = brick_device

        # TODO: better name? also, could this be neater?
        try:
            self.is_silenced = kwargs["disable_sound"]
        except KeyError:
            self.is_silenced = False

    @staticmethod
    def _configure_ports_with_mode(
        self,
        port_a=None,
        port_b=None,
        port_c=None,
        port_d=None,
        mode_for_a=None,
        mode_for_b=None,
        mode_for_c=None,
        mode_for_d=None,
    ):
        self._port_a = port_a
        if self._port_a and self._port_a.status:
            debug_logger("port_a mode: {}".format(self._port_a.mode))
            if not self._port_a.mode:
                self._port_a.mode = mode_for_a or "dc-motor"

        self._port_b = port_b
        if self._port_b and self._port_b.status:
            debug_logger("port_b mode: {}".format(self._port_b.mode))
            if not self._port_b.mode:
                self._port_b.mode = mode_for_b or "dc-motor"

        self._port_c = port_c
        if self._port_c and self._port_c.status:
            debug_logger("port_c mode: {}".format(self._port_c.mode))
            if not self._port_c.mode:
                self._port_c.mode = mode_for_c or "dc-motor"

        self._port_d = port_d
        if self._port_d and self._port_d.status:
            debug_logger("port_d mode: {}".format(self._port_d.mode))
            if not self._port_d.mode:
                self._port_d.mode = mode_for_d or "dc-motor"

        sleep(0.5)

    def run(self):
        """Run dha app :)"""

        self._console.clear()
        self._console.text_at(
            "LOOK AT DHIS '{}' SHIT".format(self.name),
            alignment="C",
            reset_console=True,
        )


class EV3App(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO: better name? also, could this be neater?
        try:
            self.is_silenced = kwargs["disable_sound"]
        except KeyError:
            self.is_silenced = False

        self._buttons = Button()
        self._console = Console()
        self._sound = Sound()

        # TODO: implement dynamic mapping safely
        port_a = kwargs["port_a"] or LegoPort("outA")
        port_b = kwargs["port_b"] or LegoPort("outB")
        self._port_c = LegoPort("outC")

        super()._configure_ports_with_mode(self, port_a=port_a, port_b=port_b)

        self._aux_motor = MediumMotor(self._port_c.address)

        self._aux_motor.on_for_rotations(50, 3)

        self._right_motor = DcMotor(self._port_a.address)
        self._left_motor = DcMotor(self._port_b.address)
        self.current_direction = "forwards"

        self._front_touch_sensor = TouchSensor(INPUT_1)
        self._back_touch_sensor = TouchSensor(INPUT_2)

    def boot_up_greeting(self):
        self.say("Bootin up, baby")
        self._console.text_at("Bootin up . . .", alignment="C")
        sleep(1)
        self._console.text_at("BINGO BANGO!", alignment="C", reset_console=True)
        self.say("BINGO BANGO!")

    def shut_down(self):
        self._console.text_at("I am a pickle!", reset_console=True, alignment="C")
        self.say("I am a pickle!")

        self._console.text_at("Bye forever", alignment="C")
        self.say("Bye forever")

    def say(self, text, **kwargs):
        if not self.is_silenced:
            self._sound.speak(text, **kwargs)

    def run(
        self,
    ):
        pass

    def drive(
        self,
        speed=None,
        right_wheel_speed=None,
        left_wheel_speed=None,
        direction="forwards",
        duration=1,
    ):
        if direction != self.current_direction:
            self.current_direction = direction

        if speed and not right_wheel_speed:
            right_wheel_speed = speed if direction == "forwards" else -speed
        if speed and not left_wheel_speed:
            left_wheel_speed = -speed if direction == "forwards" else speed

        self._right_motor.run_direct(duty_cycle_sp=right_wheel_speed)
        self._left_motor.run_direct(duty_cycle_sp=left_wheel_speed)

        if duration > 0:
            sleep(duration)
            self.stop()

    def stop(self):
        self._right_motor.stop()
        self._left_motor.stop()


class BaseCar(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._buttons = Button()
        self._console = Console()
        self._sound = Sound()
        # self._turn_speed = SpeedDPS(90)
        self._turn_speed = 100

        # TODO: implement dynamic mapping safely
        port_a = kwargs["port_a"] or LegoPort("outA")
        port_b = kwargs["port_b"] or LegoPort("outB")
        port_d = kwargs["port_d"] or LegoPort("outD")

        super()._configure_ports_with_mode(
            self, port_a=port_a, port_b=port_b, port_d=port_d
        )

        self._front_axle_motor = MediumMotor(self._port_b.address)

        self._rear_right_motor = LargeMotor(self._port_d.address)
        self._rear_left_motor = LargeMotor(self._port_a.address)

        self._front_touch_sensor = TouchSensor(INPUT_2)
        self._back_touch_sensor = TouchSensor(INPUT_1)


class EV3App_Basically_A_Car(BaseCar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        __slots__ = ["_drive_direction", "_turn_direction"]

        self._drive_direction = DriveDirection.FORWARDS.value
        self._turn_direction = TurnDirection.STRAIGHT.value

        self.cruise_speed = 45
        self.reorient_speed = 60

    @property
    def drive_direction(self):
        return self._drive_direction

    @drive_direction.setter
    def drive_direction(self, direction):
        self._drive_direction = direction

    @property
    def turn_direction(self):
        return self._turn_direction

    @turn_direction.setter
    def turn_direction(self, direction):
        self._turn_direction = direction

    def run(
        self,
    ):
        start_time = int(time())
        iteration_count = 0
        current_drive_direction = DriveDirection.FORWARDS.value
        debug_logger("Beginning at {}".format(start_time))

        while True:
            if start_time % 1000 == 0.0:
                seconds_since_start = int(time()) - start_time
                debug_logger("Running for {} seconds".format(seconds_since_start))
                iteration_count += 1

            if self.turn_direction != TurnDirection.STRAIGHT.value:
                self.turn_front_axle(turn_direction=TurnDirection.STRAIGHT.value)
            self.drive(
                speed=self.cruise_speed,
                drive_direction=current_drive_direction,
                duration=-1,
            )

            if self._front_touch_sensor.is_pressed:
                self.stop()
                current_drive_direction = DriveDirection.REVERSE.value
                turn_direction = self._choose_turn_direction(
                    drive_direction=current_drive_direction,
                    last_turn_direction=self.turn_direction,
                )
                debug_logger("Front touch sensor pressed!")
                debug_logger(
                    "turn_direction: {}\ndrive_direction: {}\ncurrent_drive_direction: {}".format(
                        turn_direction, self.drive_direction, current_drive_direction
                    )
                )
                self.say("Ouch, my face!")
                self.turn_front_axle(turn_direction=turn_direction)
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
                debug_logger("Back touch sensor pressed!")
                debug_logger(
                    "turn_direction: {}\ndrive_direction: {}\ncurrent_drive_direction: {}".format(
                        turn_direction, self.drive_direction, current_drive_direction
                    )
                )
                self.say("Ouch, my butthole!")
                self.turn_front_axle(turn_direction=turn_direction)
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
        right_wheel_speed=None,
        left_wheel_speed=None,
        drive_direction="forwards",
        duration=1,
    ):

        if drive_direction != self.drive_direction:
            debug_logger(("-" * 30) + " drive: change direction " + ("-" * 30))
            debug_logger(
                "turn_direction: {}\ndrive_direction: {}\ndrive_direction arg: {}".format(
                    self.turn_direction, self.drive_direction, drive_direction
                )
            )

        if (not right_wheel_speed and not left_wheel_speed) and speed:
            if drive_direction == DriveDirection.FORWARDS.value:
                self.forward(speed=speed)
            elif drive_direction == DriveDirection.REVERSE.value:
                self.reverse(speed=speed)
        else:
            right_wheel_speed = -speed if drive_direction == "forwards" else speed
            left_wheel_speed = -speed if drive_direction == "forwards" else speed

            self._rear_right_motor.run_direct(duty_cycle_sp=right_wheel_speed)
            self._rear_left_motor.run_direct(duty_cycle_sp=left_wheel_speed)
            if duration > 0:
                sleep(duration)

        if drive_direction != self.drive_direction:
            debug_logger(
                "speed: {}\nright_wheel_speed: {}\nleft_wheel_speed: {}".format(
                    speed, right_wheel_speed, left_wheel_speed
                )
            )
            self.drive_direction = drive_direction

    def forward(self, speed=0):
        self._rear_right_motor.run_direct(duty_cycle_sp=speed)
        self._rear_left_motor.run_direct(duty_cycle_sp=speed)

    def reverse(self, speed=0):
        self._rear_right_motor.run_direct(duty_cycle_sp=(-speed))
        self._rear_left_motor.run_direct(duty_cycle_sp=(-speed))

    def turn_front_axle(self, turn_direction):
        if turn_direction == self.turn_direction:
            return

        self.turn_direction = turn_direction

        if turn_direction == "straight":
            debug_logger("Straightenin' out!")
            self._front_axle_motor.run_to_abs_pos(
                position_sp=0, speed_sp=self._turn_speed
            )
        elif turn_direction == "left":
            debug_logger("Turnin' left!")
            self._front_axle_motor.run_to_abs_pos(
                position_sp=45, speed_sp=self._turn_speed
            )
        elif turn_direction == "right":
            debug_logger("Turnin' right!")
            self._front_axle_motor.run_to_abs_pos(
                position_sp=-45, speed_sp=self._turn_speed
            )

    def _choose_turn_direction(self, drive_direction, last_turn_direction):
        if drive_direction == "forward":
            return "right" if last_turn_direction == "left" else "left"
        else:
            return "left" if last_turn_direction == "right" else "right"

    def stop(self):
        self._rear_right_motor.stop()
        self._rear_left_motor.stop()

    def boot_up_greeting(self):
        self.say("Bootin up, baby")
        self._console.text_at("Bootin up . . .", alignment="C")
        sleep(1)
        self._console.text_at("BINGO BANGO!", alignment="C", reset_console=True)
        self.say("BINGO BANGO!")

    def shut_down(self):
        self._console.text_at("I am a pickle!", reset_console=True, alignment="C")
        self.say("I am a pickle!")

        self._console.text_at("Bye forever", alignment="C")
        self.say("Bye forever")

    def say(self, text, **kwargs):
        if self.is_silenced:
            debug_logger(text)
        else:
            self._sound.speak(text, **kwargs)


def debug_logger(*args, **kwargs):
    try:
        print(*args, file=sys.stderr, **kwargs)
    except Exception:
        pass
