from inspect import getmembers
from pprint import pprint as pretty_print
from time import sleep, time

from ev3dev2.button import Button
from ev3dev2.console import Console
from ev3dev2.motor import LargeMotor, MediumMotor
from ev3dev2.port import LegoPort
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sound import Sound

# from .constants import DriveDirection, TurnDirection
from .utils import debug_logger


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
