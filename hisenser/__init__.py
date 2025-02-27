from enum import Enum
from json import dumps, loads
from os.path import dirname, join
from queue import Empty, Queue
from ssl import _create_unverified_context
from time import monotonic, sleep
from types import TracebackType
from typing import Any, Optional, Type, Union
from uuid import uuid4

from paho.mqtt import client as mqtt


class AdaptiveContrast(int, Enum):
    OFF = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class ApplyPicture(int, Enum):
    CURRENT = 0
    ALL = 1


class ColorGamut(int, Enum):
    AUTO = 0
    NATIVE = 1


class ColorTemperature(int, Enum):
    STANDARD = 1
    WARM1 = 2
    WARM2 = 3
    COOL = 4


class GammaAdjustment(int, Enum):
    BT_1886 = 3
    GAMMA_1_8 = 4
    GAMMA_1_9 = 5
    GAMMA_2_0 = 0
    GAMMA_2_1 = 6
    GAMMA_2_2 = 1
    GAMMA_2_3 = 7
    GAMMA_2_4 = 2
    GAMMA_2_6 = 9


class HdmiFormat(str, Enum):
    STANDARD = "KEY_UP"
    ENHANCED = "KEY_DOWN"


class LocalDimming(int, Enum):
    OFF = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class NoiseReduction(int, Enum):
    OFF = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class PictureMode(str, Enum):
    STANDARD = "1"
    CINEMA_DAY = "3"
    CINEMA_NIGHT = "2"
    DYNAMIC = "0"
    SPORTS = "5"
    HDR_STANDARD = "1"
    HDR_DAY = "3"
    HDR_NIGHT = "2"
    HDR_DYNAMIC = "0"
    HDR_SPORTS = "5"
    DOLBY_VISION_BRIGHT = "3"
    DOLBY_VISION_DARK = "2"
    DOLBY_VISION_CUSTOM = "1"


class UltraSmoothMotion(int, Enum):
    OFF = 0
    SMOOTH = 5
    STANDARD = 4
    CLEAR = 3
    FILM = 2


class Client:

    def __init__(self, address: str, foolish: bool = False, secured: bool = False, timeout: Union[float, int] = 10.0):
        self.address = address
        self.foolish = foolish
        self.secured = secured
        self.timeout = timeout
        self.enabled = False
        self.deposit = Queue()
        self.macaddr = "XX:XX:XX:XX:XX:XY"
        self.secrets = "hisenseservice", "multimqttservice"

    def __enter__(self):
        self.manager = mqtt.Client(str(uuid4()))
        if self.secured:
            self.context = _create_unverified_context()
            if self.foolish:
                self.cerfile = join(dirname(__file__), "rcm_certchain_pem.cer")
                self.keyfile = join(dirname(__file__), "rcm_pem_privkey.pkcs8")
                self.context.load_cert_chain(self.cerfile, self.keyfile)
                self.manager.tls_set_context(self.context)
        self.manager.tls_insecure_set(True)
        self.manager.username_pw_set(self.secrets[0], self.secrets[1])
        self.manager.on_connect = self._on_connect
        self.manager.on_message = self._on_message
        self.manager.connect(self.address, 36669)
        self.manager.loop_start()
        startup = monotonic()
        while not self.enabled:
            sleep(0.01)
            if monotonic() - startup > self.timeout:
                raise Exception("accessing television has timeout")
        return self

    def __exit__(self, group: Optional[Type[BaseException]], value: Optional[BaseException], trace: Optional[TracebackType]):
        self.enabled = False
        if isinstance(value, Exception):
            self.manager.disconnect()
            self.manager.loop_stop()

    def _on_connect(self, *args, **kwargs):
        channel = f"/remoteapp/mobile/{self.macaddr}$normal/#"
        self.manager.subscribe(channel)
        self.enabled = True

    def _on_message(self, manager: mqtt.Client, content: Optional[Any], message: mqtt.MQTTMessage):
        payload = loads(message.payload.decode("utf-8", errors="strict")) if message.payload else message.payload
        self.deposit.put_nowait(payload)

    def attach(self) -> bool:
        try:
            self.invoke("ui_service", "gettvstate")
            self.deposit.get(block=True, timeout=3.0)
            return False
        except Empty:
            return True

    def gather(self) -> Optional[dict]:
        try:
            return self.deposit.get(block=True, timeout=self.timeout)
        except Empty as e:
            raise Exception("obtaining message has failed") from e

    def invoke(self, service: str, mission: str, payload: Optional[Union[dict, str]] = None):
        channel = f"/remoteapp/tv/{service}/{self.macaddr}$normal/actions/{mission}"
        payload = dumps(payload) if isinstance(payload, dict) else payload
        self.manager.publish(channel, payload).wait_for_publish()

    def modify(self, mission: str, section: int, content: Union[int, str], variety: str):
        self.invoke("platform_service", "picturesetting", {
            "action": mission,
            "menu_id": section,
            "menu_value": content,
            "menu_value_type": variety
        })

    def permit(self, pairing: str):
        if not pairing.isnumeric() or len(pairing) != 4:
            raise Exception("specified pairing code is invalid")
        self.invoke("ui_service", "authenticationcode", {"authNum": pairing})
        if int(self.gather()["result"]) != 1:
            raise Exception("importing pairing code has failed")

    def repeat(self, keyname: str, repeats: int = 1):
        for _ in range(repeats):
            self.invoke("remote_service", "sendkey", keyname.upper())
            sleep(0.5)

    def switch(self, pattern: str) -> Optional[dict]:
        if not pattern:
            raise Exception("specified input source is empty")
        self.invoke("ui_service", "sourcelist")
        results = [i for i in self.gather() if pattern in i["sourcename"] or pattern in i["displayname"]]
        if (payload := next(iter(results), None)) is None:
            raise Exception("specified input source is invalid")
        self.invoke("ui_service", "changesource", payload)
        return payload

    def change_adaptive_contrast(self, payload: AdaptiveContrast):
        self.modify("set_value", 29, payload, "int")

    def change_apply_picture(self, payload: ApplyPicture):
        self.modify("set_value", 85, payload, "int")

    def change_backlight(self, payload: int):
        self.modify("set_value", 8, payload, "int")

    def change_brightness(self, payload: int):
        self.modify("set_value", 3, payload, "int")

    def change_color_gamut(self, payload: ColorGamut):
        self.modify("set_value", 52, payload, "int")

    def change_color_temperature(self, payload: ColorTemperature):
        self.modify("set_value", 30, payload, "int")

    def change_color_saturation(self, payload: int):
        self.modify("set_value", 5, payload, "int")

    def change_contrast(self, payload: int):
        self.modify("set_value", 4, payload, "int")

    def enable_game_mode(self, enabled: bool):
        self.modify("set_value", 122, 1 if enabled else 0, "int")

    def change_gamma_adjustment(self, payload: GammaAdjustment):
        self.modify("set_value", 77, payload, "int")

    def change_hdmi_format(self, payload: HdmiFormat):
        self.repeat("key_menu")
        self.repeat("key_down", 2)
        self.repeat("key_ok")
        self.repeat("key_down", 5)
        self.repeat("key_ok")
        self.repeat("key_down", 11)
        self.repeat("key_up", 2)
        self.repeat("key_ok", 2)
        self.repeat(payload, 2)
        self.repeat("key_ok")
        sleep(2)
        self.repeat("key_returns", 5)

    def change_local_dimming(self, payload: LocalDimming):
        self.modify("set_value", 27, payload, "int")

    def change_noise_reduction(self, payload: NoiseReduction):
        self.modify("set_value", 25, payload, "int")
        self.modify("set_value", 26, payload, "int")

    def change_picture_mode(self, payload: PictureMode):
        self.modify("on_action", 1, payload, "string")

    def change_sharpness(self, payload: int):
        self.modify("set_value", 21, payload * 2, "int")

    def change_ultra_smooth_motion(self, payload: UltraSmoothMotion):
        self.modify("set_value", 23, payload, "int")

    def change_white_balance(self, r_offset: int, g_offset: int, b_offset: int, r_gain: int, g_gain: int, b_gain: int):
        self.revert_white_balance()
        self.modify("set_value", 35, r_offset, "int")
        self.modify("set_value", 36, g_offset, "int")
        self.modify("set_value", 37, b_offset, "int")
        self.modify("set_value", 32, r_gain, "int")
        self.modify("set_value", 33, g_gain, "int")
        self.modify("set_value", 34, b_gain, "int")

    def revert_picture_mode(self):
        self.modify("on_action", 104, "-1", "string")

    def revert_white_balance(self):
        self.modify("set_value", 43, 0, "int")
        self.modify("on_action", 100, "-1", "string")

    def toggle_viewing_angle(self):
        self.repeat("key_menu")
        self.repeat("key_down", 2)
        self.repeat("key_ok", 2)
        self.repeat("key_down", 5)
        self.repeat("key_ok")
        self.repeat("key_down", 20)
        self.repeat("key_up", 2)
        self.repeat("key_ok")
        self.repeat("key_down", 10)
        self.repeat("key_up")
        self.repeat("key_ok")
        self.repeat("key_returns", 5)
