import enum
import time

port = 'COM3'  # 根据实际情况修改端口号
baud_rate = 9600  # 波特率
timeout = 1  # 读超时

HEAD = bytearray.fromhex("57 AB")
ADDR = bytearray.fromhex("00")


class CMD(enum.Enum):
    # 获取芯片版本等信息
    CMD_GET_INFO = bytearray.fromhex("01")
    # 发送USB键盘普通数据
    CMD_SEND_KB_GENERAL_DATA = bytearray.fromhex("02")
    # 发送USB键盘多媒体数据
    CMD_SEND_KB_MEDIA_DATA = bytearray.fromhex("03")
    # 发送USB绝对鼠标数据
    CMD_SEND_MS_ABS_DATA = bytearray.fromhex("04")
    # 发送USB相对鼠标数据
    CMD_SEND_MS_REL_DATA = bytearray.fromhex("05")
    # 发送USB自定义HID设备数据
    CMD_SEND_MY_HID_DATA = bytearray.fromhex("06")
    # 读取USB自定义HID设备数据
    CMD_READ_MY_HID_DATA = bytearray.fromhex("07")
    # 获取参数配置
    CMD_GET_PARA_CFG = bytearray.fromhex("08")
    # 设置参数配置
    CMD_SET_PARA_CFG = bytearray.fromhex("09")
    # 获取字符串描述符配置
    CMD_GET_USB_STRING = bytearray.fromhex("0A")
    # 设置字符串描述符配置
    CMD_SET_USB_STRING = bytearray.fromhex("0B")
    # 恢复出厂默认配置
    CMD_SET_DEFAULT_CFG = bytearray.fromhex("0C")
    # 复位芯片
    CMD_RESET = bytearray.fromhex("0F")


class ReplyStatus(enum.Enum):
    DEF_CMD_SUCCESS = 0x00
    DEF_CMD_ERR_TIMEOUT = 0xE1
    DEF_CMD_ERR_HEAD = 0xE2
    DEF_CMD_ERR_CMD = 0xE3
    DEF_CMD_ERR_SUM = 0xE4
    DEF_CMD_ERR_PARA = 0xE5
    DEF_CMD_ERR_OPERATE = 0xE6
    UNAVAILABLE_REPLY = 0xFF


def get_reply_status(cmd_code: bytearray, reply_bytes: bytearray) -> ReplyStatus:
    if reply_bytes[3] == cmd_code[0] | 0x80:
        return ReplyStatus.DEF_CMD_SUCCESS
    elif reply_bytes == cmd_code[0] | 0xc0:
        return ReplyStatus(reply_bytes[5])
    else:
        return ReplyStatus.UNAVAILABLE_REPLY


def get_check_sum(cmd: bytearray, data_len: bytearray, data: bytearray) -> bytearray:
    return bytearray([sum(HEAD + ADDR + cmd + data_len + data) & 0xFF])


def compose_packet(cmd: bytearray, data_len: bytearray, data: bytearray, check_sum: bytearray) -> bytearray:
    return HEAD + ADDR + cmd + data_len + data + check_sum


def reset(ser):
    check_sum = get_check_sum(CMD.CMD_RESET.value, bytearray.fromhex("00"), bytearray.fromhex(""))
    ser.write(compose_packet(CMD.CMD_RESET.value, bytearray.fromhex("00"), bytearray.fromhex(""), check_sum))
    time.sleep(0.5)
