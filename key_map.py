import enum
import time

from serial import Serial
from common import logger

from common import get_check_sum, compose_packet, get_reply_status, CMD, ReplyStatus


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
        Key_Shift = bytearray.fromhex("E1")
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

    key_map = {
        "a": [Key.Key_A, Control.NULL],
        "b": [Key.Key_B, Control.NULL],
        "c": [Key.Key_C, Control.NULL],
        "d": [Key.Key_D, Control.NULL],
        "e": [Key.Key_E, Control.NULL],
        "f": [Key.Key_F, Control.NULL],
        "g": [Key.Key_G, Control.NULL],
        "h": [Key.Key_H, Control.NULL],
        "i": [Key.Key_I, Control.NULL],
        "j": [Key.Key_J, Control.NULL],
        "k": [Key.Key_K, Control.NULL],
        "l": [Key.Key_L, Control.NULL],
        "m": [Key.Key_M, Control.NULL],
        "n": [Key.Key_N, Control.NULL],
        "o": [Key.Key_O, Control.NULL],
        "p": [Key.Key_P, Control.NULL],
        "q": [Key.Key_Q, Control.NULL],
        "r": [Key.Key_R, Control.NULL],
        "s": [Key.Key_S, Control.NULL],
        "t": [Key.Key_T, Control.NULL],
        "u": [Key.Key_U, Control.NULL],
        "v": [Key.Key_V, Control.NULL],
        "w": [Key.Key_W, Control.NULL],
        "x": [Key.Key_X, Control.NULL],
        "y": [Key.Key_Y, Control.NULL],
        "z": [Key.Key_Z, Control.NULL],

        "A": [Key.Key_A, Control.L_SHIFT],
        "B": [Key.Key_B, Control.L_SHIFT],
        "C": [Key.Key_C, Control.L_SHIFT],
        "D": [Key.Key_D, Control.L_SHIFT],
        "E": [Key.Key_E, Control.L_SHIFT],
        "F": [Key.Key_F, Control.L_SHIFT],
        "G": [Key.Key_G, Control.L_SHIFT],
        "H": [Key.Key_H, Control.L_SHIFT],
        "I": [Key.Key_I, Control.L_SHIFT],
        "J": [Key.Key_J, Control.L_SHIFT],
        "K": [Key.Key_K, Control.L_SHIFT],
        "L": [Key.Key_L, Control.L_SHIFT],
        "M": [Key.Key_M, Control.L_SHIFT],
        "N": [Key.Key_N, Control.L_SHIFT],
        "O": [Key.Key_O, Control.L_SHIFT],
        "P": [Key.Key_P, Control.L_SHIFT],
        "Q": [Key.Key_Q, Control.L_SHIFT],
        "R": [Key.Key_R, Control.L_SHIFT],
        "S": [Key.Key_S, Control.L_SHIFT],
        "T": [Key.Key_T, Control.L_SHIFT],
        "U": [Key.Key_U, Control.L_SHIFT],
        "V": [Key.Key_V, Control.L_SHIFT],
        "W": [Key.Key_W, Control.L_SHIFT],
        "X": [Key.Key_X, Control.L_SHIFT],
        "Y": [Key.Key_Y, Control.L_SHIFT],
        "Z": [Key.Key_Z, Control.L_SHIFT],

        "1": [Key.Key_1, Control.NULL],
        "2": [Key.Key_2, Control.NULL],
        "3": [Key.Key_3, Control.NULL],
        "4": [Key.Key_4, Control.NULL],
        "5": [Key.Key_5, Control.NULL],
        "6": [Key.Key_6, Control.NULL],
        "7": [Key.Key_7, Control.NULL],
        "8": [Key.Key_8, Control.NULL],
        "9": [Key.Key_9, Control.NULL],
        "0": [Key.Key_0, Control.NULL],

        "!": [Key.Key_1, Control.L_SHIFT],
        "@": [Key.Key_2, Control.L_SHIFT],
        "#": [Key.Key_3, Control.L_SHIFT],
        "$": [Key.Key_4, Control.L_SHIFT],
        "%": [Key.Key_5, Control.L_SHIFT],
        "^": [Key.Key_6, Control.L_SHIFT],
        "&": [Key.Key_7, Control.L_SHIFT],
        "*": [Key.Key_8, Control.L_SHIFT],
        "(": [Key.Key_9, Control.L_SHIFT],
        ")": [Key.Key_0, Control.L_SHIFT],

        "-": [Key.Key_Minus, Control.NULL],
        "_": [Key.Key_Minus, Control.L_SHIFT],

        "=": [Key.Key_Plus, Control.NULL],
        "+": [Key.Key_Plus, Control.L_SHIFT],

        "[": [Key.Key_Bracket_Left, Control.NULL],
        "{": [Key.Key_Bracket_Left, Control.L_SHIFT],

        "]": [Key.Key_Bracket_Right, Control.NULL],
        "}": [Key.Key_Bracket_Right, Control.L_SHIFT],

        ";": [Key.Key_Colon, Control.NULL],
        ":": [Key.Key_Colon, Control.L_SHIFT],

        "'": [Key.Key_Quote, Control.NULL],
        '"': [Key.Key_Quote, Control.L_SHIFT],

        ",": [Key.Key_Less, Control.NULL],
        "<": [Key.Key_Less, Control.L_SHIFT],

        ".": [Key.Key_Greater, Control.NULL],
        ">": [Key.Key_Greater, Control.L_SHIFT],

        "/": [Key.Key_Question, Control.NULL],
        "?": [Key.Key_Question, Control.L_SHIFT],

        "`": [Key.Key_Tilde, Control.NULL],
        "~": [Key.Key_Tilde, Control.L_SHIFT],

        " ": [Key.Key_Space, Control.NULL]

    }

    def __init__(self, ser: Serial):
        self.ser = ser

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
            logger.warning("键盘最多只能输入6个键")
        for key in data:
            keyboard_data += key.value
        if len(keyboard_data) < 8:
            keyboard_data += bytearray.fromhex("00") * (8 - len(keyboard_data))
        else:
            keyboard_data = keyboard_data[:8]
        check_sum = get_check_sum(keyboard_cmd, data_len, keyboard_data)
        packet = compose_packet(keyboard_cmd, data_len, keyboard_data, check_sum)
        logger.info(f"发送数据包: {packet.hex(sep=' ')}")
        self.ser.write(packet)

        time.sleep(0.1)
        received_data = self.ser.read(self.ser.in_waiting)  # 读取所有可用的数据
        if received_data:
            logger.info(f"接收到的数据包: {received_data.hex(sep=' ')}")
            reply_code = bytearray(received_data)
            return get_reply_status(keyboard_cmd, reply_code)
        else:
            logger.error("没有收到回复")
            return ReplyStatus.UNAVAILABLE_REPLY

    def release(self):
        return self.send_data([self.Key.RELEASE], self.Control.NULL)

    def input_string(self, s: str):
        for c in s:
            command = self.key_map.get(c, None)
            if command is None:
                logger.error(f"不兼容的字符:{c}")
                return
            self.send_data([command[0]], ctrl=command[1])
            self.release()

    def press_enter_key(self):
        self.send_data([self.Key.Key_Enter])
        self.release()

    def press_shift_key(self):
        self.send_data([self.Key.Key_Shift])
        self.release()

    def press_space_key(self):
        self.send_data([self.Key.Key_Space])
        self.release()

    def press_backspace_key(self):
        self.send_data([self.Key.Key_Backspace])
        self.release()

    def press_tab_key(self):
        self.send_data([self.Key.Key_Tab])
        self.release()

    def maximize(self):
        self.send_data([self.Key.Key_Up], self.Control.L_WIN)
        self.release()

    def fullscreen(self):
        self.send_data([self.Key.Key_F11])
        self.release()

    def close(self):
        self.send_data([self.Key.Key_F4], self.Control.L_ALT)
        self.release()

    def back_desktop(self):
        self.send_data([self.Key.Key_D], self.Control.L_WIN)
        self.release()

    def switch_input(self):
        self.send_data([self.Key.Key_Space], self.Control.L_CTRL)
        self.release()
