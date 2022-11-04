import sys
from inspect import getmembers
from time import sleep

from ev3dev2.button import Button
from ev3dev2.console import Console
from ev3dev2.motor import DcMotor
from ev3dev2.port import LegoPort
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sound import Sound


class App:
    _brick_device = None
    _console = None
    _port_a = None
    _port_b = None
    _console = None
    _buttons = None
    _sound = None

    def __init__(self, name="", brick_device=None):
        self.name = name

        self._brick_device = brick_device

        # self._port_a = LegoPort("outA")
        # self._port_b = LegoPort("outB")
        # self._console = Console()
        # self._buttons = Button()
        # self._sound = Sound()

        # assert self._port_a and self._port_a.status
        # assert self._port_b and self._port_b.status
        # self._port_a.mode = "dc-motor"
        # self._port_b.mode = "dc-motor"
        # sleep(0.5)
        # self._right_motor = DcMotor(self._port_a.address)
        # self._left_motor = DcMotor(self._port_b.address)

    @staticmethod
    def _configure_ports_with_mode(
        self, port_a=None, port_b=None, mode_for_a=None, mode_for_b=None
    ):
        self._port_a = port_a
        assert self._port_a and self._port_a.status
        if not self._port_a.mode:
            self._port_a.mode = mode_for_a or "dc-motor"

        self._port_b = port_b
        assert self._port_b and self._port_b.status
        if not self._port_b.mode:
            self._port_b.mode = mode_for_b or "dc-motor"

        sleep(0.5)

    def run(self):
        """Run dha app :)"""

        self._console.clear()
        self._console.text_at(
            "LOOK AT DHIS '{}' SHIT".format(self.name),
            alignment="C",
            reset_console=True,
        )
        # try:
        #     self._brick_device.display.text(f"LOOK AT DHIS '{self.name}' SHIT")
        # except Exception:
        #     print("guess it doesn't like f-strings?")
        #     self._brick_device.display.text("LOOK AT DHIS '{}' SHIT".format(self.name))


class EV3App(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._buttons = Button()
        self._console = Console()
        self._sound = Sound()

        super()._configure_ports_with_mode(
            self, port_a=LegoPort("outA"), port_b=LegoPort("outB")
        )

        self._right_motor = DcMotor(self._port_a.address)
        self._left_motor = DcMotor(self._port_b.address)

        self._front_touch_sensor = TouchSensor(INPUT_1)
        self._back_touch_sensor = TouchSensor(INPUT_2)

    def run(
        self,
    ):
        pass

    def boot_up_greeting(self):
        self._sound.speak("Bootin up, baby")
        self._console.text_at("Bootin up . . .", alignment="C")
        sleep(1)
        self._console.text_at("BINGO BANGO!", alignment="C", reset_console=True)
        self._sound.speak("BINGO BANGO!")

    def shut_down(self):
        self._console.text_at("I am a pickle!", reset_console=True, alignment="C")
        self._sound.speak("I am a pickle!")

        self._console.text_at("Bye forever", alignment="C")
        self._sound.speak("Bye forever")

    def drive(
        self,
        speed=None,
        right_wheel_speed=None,
        left_wheel_speed=None,
        direction="forwards",
        duration=1,
    ):
        if speed and not right_wheel_speed:
            right_wheel_speed = speed if direction == "forwards" else -speed
        if speed and not left_wheel_speed:
            left_wheel_speed = -speed if direction == "forwards" else speed

        self._right_motor.run_direct(duty_cycle_sp=right_wheel_speed)
        self._left_motor.run_direct(duty_cycle_sp=left_wheel_speed)

        if duration > 0:
            sleep(duration)
            self._right_motor.stop()
            self._left_motor.stop()
