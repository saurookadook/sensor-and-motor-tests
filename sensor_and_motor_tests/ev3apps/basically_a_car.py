from pprint import pprint as pretty_print
from time import sleep, time

from ..app import BaseCar
from ..constants import DriveDirection, TurnDirection
from ..utils import debug_logger


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
                self.reset_drive_motors()
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
                self.reset_drive_motors()
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
        speed = -speed
        self._base_run_direct(speed=speed)

    def reverse(self, speed=0):
        self._base_run_direct(speed=speed)

    def reset_drive_motors(self):
        self._rear_right_motor.reset()
        self._rear_left_motor.reset()

    def _base_run_direct(self, speed=0):
        self._rear_right_motor.run_direct(duty_cycle_sp=speed)
        self._rear_left_motor.run_direct(duty_cycle_sp=speed)

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
