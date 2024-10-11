import enum
import time
from serial import Serial
from common import logger
from common import CMD, get_check_sum, compose_packet, get_reply_status, ReplyStatus


class Mouse:
    class MouseButton(enum.Enum):
        NULL = bytearray.fromhex("00")
        Button_Left = bytearray.fromhex("01")
        Button_Right = bytearray.fromhex("02")
        Button_Middle = bytearray.fromhex("04")

    def __init__(self, screen_width: int, screen_height: int, ser: Serial):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.ser = ser
        self.x_cur = 0
        self.y_cur = 0
        self.wheel_cur = 0

    def send_data_absolute(self, x: int, y: int, wheel: int = 0, ctrl: MouseButton = MouseButton.NULL):
        if x >= self.screen_width:
            logger.warning("鼠标x坐标超出屏幕范围，将截断")
            x = self.screen_width
        if y >= self.screen_height:
            logger.warning("鼠标y坐标超出屏幕范围，将截断")
            y = self.screen_height
        if wheel >= 128:
            logger.warning("滚轮数据超出范围，将截断,最大值为-127~128")
            wheel = 127

        self.x_cur = x
        self.y_cur = y
        # 将字符转写为数据包
        mouse_absolute_cmd = CMD.CMD_SEND_MS_ABS_DATA.value
        data_len = bytearray.fromhex("07")  # 数据长度7个字节
        # 第1个字节必须为0x02
        mouse_data = bytearray.fromhex("02")
        # 第2个字节，鼠标按键
        mouse_data += ctrl.value
        x_scaled = (4096 * x) // self.screen_width
        y_scaled = (4096 * y) // self.screen_height
        # 第3、4个字节x坐标
        mouse_data += x_scaled.to_bytes(2, byteorder='little')
        # 第5、6个字节y坐标
        mouse_data += y_scaled.to_bytes(2, byteorder='little')
        # 第7个字节滚轮坐标
        if wheel == 0:
            mouse_data += bytearray.fromhex("00")
        elif wheel < 0:  # 有符号的一个字节数据为[-128，127]所以xy的值不能大于127
            mouse_data += (0 - abs(x)).to_bytes(1, byteorder='big', signed=True)
        else:
            mouse_data += x.to_bytes(1, byteorder='big', signed=True)
        self.wheel_cur = wheel

        check_sum = get_check_sum(mouse_absolute_cmd, data_len, mouse_data)
        packet = compose_packet(mouse_absolute_cmd, data_len, mouse_data, check_sum)
        logger.info(f"发送数据包: {packet.hex(sep=' ')}")
        self.ser.write(packet)
        time.sleep(0.1)
        received_data = self.ser.read(self.ser.in_waiting)  # 读取所有可用的数据
        if received_data:
            logger.info(f"接收到的数据包: {received_data.hex(sep=' ')}")
            reply_code = bytearray(received_data)
            return get_reply_status(mouse_absolute_cmd, reply_code)
        else:
            logger.error("没有收到回复")
            return ReplyStatus.UNAVAILABLE_REPLY

    def send_data_relatively(self, x: int, y: int, wheel: int = 0, ctrl: MouseButton = MouseButton.NULL):
        # 将字符转写为数据包
        if abs(x) >= 128:
            logger.warning("鼠标x坐标超出范围，将截断")
            x = 127 * (x // abs(x))
        if abs(y) >= 128:
            logger.warning("鼠标y坐标超出范围，将截断")
            y = 127 * (y // abs(y))
        if wheel >= 128:
            logger.warning("滚轮数据超出范围，将截断")
            wheel = 127
        mouse_relative_cmd = CMD.CMD_SEND_MS_REL_DATA.value
        data_len = bytearray.fromhex("05")  # 数据长度7个字节
        # 第1个字节必须为0x01
        mouse_data = bytearray.fromhex("01")
        # 第2个字节鼠标按键
        mouse_data += ctrl.value
        # 第3个字节，x坐标
        if x == 0:
            mouse_data += bytearray.fromhex("00")
        elif x < 0:  # 有符号的一个字节数据为[-128，127]所以xy的值不能大于127
            mouse_data += (0 - abs(x)).to_bytes(1, byteorder='big', signed=True)
        else:
            mouse_data += x.to_bytes(1, byteorder='big', signed=True)
        # 第4个字节y坐标
        if y == 0:  # xy的值不能大于[-127,128]
            mouse_data += bytearray.fromhex("00")
        elif y < 0:
            mouse_data += (0 - abs(y)).to_bytes(1, byteorder='big', signed=True)
        else:
            mouse_data += y.to_bytes(1, byteorder='big', signed=True)
        # 第5个字节滚轮坐标
        if wheel == 0:
            mouse_data += bytearray.fromhex("00")
        elif wheel < 0:  # 有符号的一个字节数据为[-128，127]所以xy的值不能大于127
            mouse_data += (0 - abs(x)).to_bytes(1, byteorder='big', signed=True)
        else:
            mouse_data += x.to_bytes(1, byteorder='big', signed=True)
        check_sum = get_check_sum(mouse_relative_cmd, data_len, mouse_data)
        packet = compose_packet(mouse_relative_cmd, data_len, mouse_data, check_sum)
        logger.info(f"发送数据包: {packet.hex(sep=' ')}")
        self.ser.write(packet)
        time.sleep(0.05)
        received_data = self.ser.read(self.ser.in_waiting)  # 读取所有可用的数据
        if received_data:
            logger.info(f"接收到的数据包: {received_data.hex(sep=' ')}")
            return get_reply_status(mouse_relative_cmd, bytearray(received_data))
        else:
            logger.error("没有收到回复")
            return ReplyStatus.UNAVAILABLE_REPLY

    def left_button_click(self):
        self.send_data_relatively(0, 0, 0, Mouse.MouseButton.Button_Left)
        self.send_data_relatively(0, 0, 0, Mouse.MouseButton.NULL)

    def right_button_click(self):
        self.send_data_absolute(0, 0, 0, Mouse.MouseButton.Button_Right)
        self.send_data_absolute(0, 0, 0, Mouse.MouseButton.NULL)

    def middle_button_click(self):
        self.send_data_absolute(0, 0, 0, Mouse.MouseButton.Button_Middle)
        self.send_data_absolute(0, 0, 0, Mouse.MouseButton.NULL)

    def left_button_double_click(self):
        # x_save = self.x_cur
        # y_save = self.y_cur
        # wheel_save = self.wheel_cur
        self.send_data_absolute(0, 0, 0, Mouse.MouseButton.Button_Left)
        self.send_data_absolute(0, 0, 0, Mouse.MouseButton.NULL)
        self.send_data_absolute(0, 0, 0, Mouse.MouseButton.Button_Left)
        self.send_data_absolute(0, 0, 0, Mouse.MouseButton.NULL)
        # 恢复坐标
        # self.send_data_absolute(x_save, y_save, wheel_save, Mouse.MouseButtonMap.NULL)
