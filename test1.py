# 测试自动化系统验收流程

import time
from datetime import datetime

import serial

from key_map import KeyBoard
from mouse_map import Mouse
from common import logger

ser = serial.Serial('/dev/tty.usbserial-14130', 9600)  # 开启串口

mouse = Mouse(screen_width=1920, screen_height=1080, ser=ser)
keyboard = KeyBoard(ser)
# 1.打开浏览器
logger.warning("1.打开浏览器")
mouse.send_data_absolute(37, 542)
mouse.left_button_double_click()
time.sleep(2)
# 最大化浏览器（根据当前浏览器行为酌情选择）
# keyboard.maximize()
# time.sleep(2)

# 2. 输入地址
logger.warning("2.输入地址")
mouse.send_data_absolute(312, 52)
mouse.left_button_click()
time.sleep(0.5)
# 输入法调整为英文(根据操作系统输入法酌情选择)
keyboard.press_shift_key()
keyboard.input_string("http://111.48.54.19:2024/cmcsbase/#/")
keyboard.press_enter_key()
time.sleep(2)

# 3.输入用户名
logger.warning("3.输入用户名")
keyboard.press_tab_key()
keyboard.input_string("admin")
time.sleep(0.5)

# 4.输入密码
logger.warning("4.输入密码")
keyboard.press_tab_key()
keyboard.input_string("Bossien1234!@")
time.sleep(0.5)

# 5.滑动解锁
logger.warning("5.滑动解锁")
mouse.send_data_absolute(738, 582, 0, ctrl=Mouse.MouseButton.Button_Left)
mouse.send_data_absolute(1200, 581, 0, ctrl=Mouse.MouseButton.Button_Left)
time.sleep(0.5)

# 6.点击登录
logger.warning("6.点击【登录】")
mouse.send_data_absolute(940, 700)
mouse.left_button_double_click()
time.sleep(2)  # 等待加载完成

# 7. F11全屏
logger.warning("7.全屏")
mouse.left_button_click()
keyboard.fullscreen()
time.sleep(1)

# 8.点击质量验收菜单
logger.warning("8.点击【质量验收】菜单")
mouse.send_data_absolute(60, 420)
mouse.left_button_click()
time.sleep(0.5)

# 9.点击其它化验信息
logger.warning("9.点击【质量验收/其它化验信息】菜单")
mouse.send_data_absolute(78, 672)
mouse.left_button_click()
time.sleep(1)

# 10.点击新增
logger.warning("10.点击【新增】")
mouse.send_data_absolute(253, 221)
mouse.left_button_click()
time.sleep(1)

logger.warning("11.选择批次号")
# 点击批次号明细
mouse.send_data_absolute(1224, 135)
mouse.left_button_click()
time.sleep(1)

# 选择批次号
mouse.send_data_absolute(414, 337)
mouse.left_button_click()
mouse.send_data_absolute(1508, 830)
mouse.left_button_click()
time.sleep(0.5)

# 填写化验人/化验单位(自动带入)
# mouse.send_data_absolute(293, 217)
# mouse.left_button_click()
# keyboard.input_string("SSZUWQ")
# time.sleep(1)

# 12.输入化验单接收人
logger.warning("12.选择化验单接收人")
mouse.send_data_absolute(1224, 220)
mouse.left_button_click()
time.sleep(0.5)
mouse.send_data_absolute(704, 330)
mouse.left_button_click()
time.sleep(0.5)
mouse.send_data_absolute(1407, 898)
mouse.left_button_click()
time.sleep(0.5)

# 13.填写化验时间
logger.warning("13.填写化验时间")
time_str = datetime.now().strftime("%Y-%m-%d %H:%M")
mouse.send_data_absolute(332, 304)
mouse.left_button_click()
time.sleep(0.5)
keyboard.input_string(time_str)
mouse.send_data_absolute(417, 617)
mouse.left_button_click()
time.sleep(1)

# 14.填写验收样/化验单接收时间
logger.warning("14.填写接收时间")
mouse.send_data_absolute(1231, 305)
mouse.left_button_click()
keyboard.input_string("2024-10-11 13:34")
mouse.send_data_absolute(1010, 617)
mouse.left_button_click()
time.sleep(1)

# 15. 输入备注
logger.warning("15.填写备注")
mouse.send_data_absolute(110, 395)
mouse.left_button_click()
keyboard.input_string("It is a test remark")
time.sleep(0.5)
# 16. 点击【计算】
logger.warning("16.计算")
mouse.send_data_absolute(1783, 473)
mouse.left_button_click()
time.sleep(0.5)
# 17.点击确定
logger.warning("17.点击确认")
mouse.send_data_absolute(1865, 1064)
mouse.left_button_click()

logger.warning("18.完成录入")
# 10秒后关闭浏览器
time.sleep(10)
keyboard.close()

logger.warning("19.关闭浏览器")

ser.close()  # 关闭串口
