import enum
import time
import warnings

from serial import Serial

from common import get_check_sum, compose_packet, get_reply_status, CMD


class KeyBoard:
    class Key(enum.Enum):
        RELEASE = bytearray.fromhex("00")
        Key_1 = bytearray.fromhex("1E")
        Key_2 = bytearray.fromhex("1F")
        Key_3 = bytearray.fromhex("20")
        Key_4 = bytearray.fromhex("21")
        Key_5 = bytearray.fromhex("22")
        Key_6 = bytearray.fromhex("23")
        Key_7 = bytearray.fromhex("24")
        Key_8 = bytearray.fromhex("25")
        Key_9 = bytearray.fromhex("26")
        Key_0 = bytearray.fromhex("27")
        Key_Enter = bytearray.fromhex("28")
        Key_ESC = bytearray.fromhex("29")
        Key_Minus = bytearray.fromhex("2D")  # -_
        Key_Plus = bytearray.fromhex("2E")  # =+
        Key_Backspace = bytearray.fromhex("2A")
        Key_Tab = bytearray.fromhex("2B")
        Key_Space = bytearray.fromhex("2C")
        Key_CapsLock = bytearray.fromhex("39")
        Key_Colon = bytearray.fromhex("33")  # :;
        Key_Quote = bytearray.fromhex("34")  # "'
        Key_Delete = bytearray.fromhex("4C")
        Key_Greater = bytearray.fromhex("37")  # >.
        Key_Less = bytearray.fromhex("36")  # <,
        Key_Question = bytearray.fromhex("38")  # ？/
        Key_Bracket_Left = bytearray.fromhex("2F")  # [{
        Key_Bracket_Right = bytearray.fromhex("30")  # ]}
        Key_Tilde = bytearray.fromhex("35")  # ~`
        Key_Win = bytearray.fromhex("E3")  # win
        Key_Backslash = bytearray.fromhex("31")  # \|

        Key_Up = bytearray.fromhex("52")
        Key_Down = bytearray.fromhex("51")
        Key_Left = bytearray.fromhex("50")
        Key_Right = bytearray.fromhex("4F")

        Key_A = bytearray.fromhex("04")
        Key_B = bytearray.fromhex("05")
        Key_C = bytearray.fromhex("06")
        Key_D = bytearray.fromhex("07")
        Key_E = bytearray.fromhex("08")
        Key_F = bytearray.fromhex("09")
        Key_G = bytearray.fromhex("0A")
        Key_H = bytearray.fromhex("0B")
        Key_I = bytearray.fromhex("0C")
        Key_J = bytearray.fromhex("0D")
        Key_K = bytearray.fromhex("0E")
        Key_L = bytearray.fromhex("0F")
        Key_M = bytearray.fromhex("10")
        Key_N = bytearray.fromhex("11")
        Key_O = bytearray.fromhex("12")
        Key_P = bytearray.fromhex("13")
        Key_Q = bytearray.fromhex("14")
        Key_R = bytearray.fromhex("15")
        Key_S = bytearray.fromhex("16")
        Key_T = bytearray.fromhex("17")
        Key_U = bytearray.fromhex("18")
        Key_V = bytearray.fromhex("19")
        Key_W = bytearray.fromhex("1A")
        Key_X = bytearray.fromhex("1B")
        Key_Y = bytearray.fromhex("1C")
        Key_Z = bytearray.fromhex("1D")
        Key_F1 = bytearray.fromhex("3A")
        Key_F2 = bytearray.fromhex("3B")
        Key_F3 = bytearray.fromhex("3C")
        Key_F4 = bytearray.fromhex("3D")
        Key_F5 = bytearray.fromhex("3E")
        Key_F6 = bytearray.fromhex("3F")
        Key_F7 = bytearray.fromhex("40")
        Key_F8 = bytearray.fromhex("41")
        Key_F9 = bytearray.fromhex("42")
        Key_F10 = bytearray.fromhex("43")
        Key_F11 = bytearray.fromhex("44")
        Key_F12 = bytearray.fromhex("45")

    class Control(enum.Enum):
        NULL = bytearray.fromhex("00")
        R_WIN = bytearray.fromhex("80")
        R_ALT = bytearray.fromhex("40")
        R_SHIFT = bytearray.fromhex("20")
        R_CTRL = bytearray.fromhex("10")
        L_WIN = bytearray.fromhex("08")
        L_ALT = bytearray.fromhex("04")
        L_SHIFT = bytearray.fromhex("02")
        L_CTRL = bytearray.fromhex("01")

    def __init__(self, ser: Serial):
        self._ser = ser

    def send_data(self, data: list[Key], ctrl: Control = Control.NULL):
        # 将字符转写为数据包
        keyboard_cmd = CMD.CMD_SEND_KB_GENERAL_DATA.value
        data_len = bytearray.fromhex("08")  # 数据长度8个字节
        keyboard_data = bytearray.fromhex("")

        # 第1个字节：控制键
        keyboard_data += ctrl.value
        # 第2个字节：DATA固定码
        keyboard_data += bytearray.fromhex("00")
        # 第3到8个字节
        if len(data) > 6:
            warnings.warn("键盘最多只能输入6个键")
        for key in data:
            keyboard_data += key.value
        if len(keyboard_data) < 8:
            keyboard_data += bytearray.fromhex("00") * (8 - len(keyboard_data))
        else:
            keyboard_data = keyboard_data[:8]
        check_sum = get_check_sum(keyboard_cmd, data_len, keyboard_data)
        packet = compose_packet(keyboard_cmd, data_len, keyboard_data, check_sum)
        print(packet.hex(sep=" "))
        self._ser.write(packet)

        time.sleep(0.1)
        received_data = self._ser.read(self._ser.in_waiting)  # 读取所有可用的数据
        if received_data:
            print("接收到的数据:", received_data.hex(sep=" "))
        reply_code = bytearray(received_data)
        return get_reply_status(keyboard_cmd, reply_code)

    def release(self):
        return self.send_data([self.Key.RELEASE], self.Control.NULL)
