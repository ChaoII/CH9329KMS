import time
from datetime import datetime

import serial

from mouse_map import Mouse
from key_map import KeyBoard

ser = serial.Serial('/dev/tty.usbserial-14130', 9600)  # 开启串口

mouse = Mouse(screen_width=1920, screen_height=1080, ser=ser)
keyboard = KeyBoard(ser)

# 1.打开浏览器
mouse.send_data_absolute(37, 542)
mouse.left_button_double_click()

time.sleep(2)
keyboard.send_data([KeyBoard.Key.Key_Up], KeyBoard.Control.L_WIN)
time.sleep(5)
# 2. 点击地址栏输入地址
mouse.send_data_absolute(312, 52)
mouse.left_button_click()

# time.sleep(1)
# # 输入法调整为英文
# keyboard.switch_input()
# time.sleep(1)
# 3. 输入地址
keyboard.input_string("http://111.48.54.19:2024/cmcsbase/#/")
keyboard.press_enter_key()
time.sleep(5)

# # 4.输入用户名
# keyboard.press_tab_key()
# keyboard.input_string("admin")
#
# # 5.输入密码
# keyboard.press_tab_key()
# keyboard.input_string("Bossien1234!@")
#
# # 6.滑动解锁
# mouse.send_data_absolute(738, 582, 0, ctrl=Mouse.MouseButton.Button_Left)
# mouse.send_data_absolute(1200, 581, 0, ctrl=Mouse.MouseButton.Button_Left)
# # 7.点击登录
# mouse.send_data_absolute(940, 700)
# mouse.left_button_double_click()
# time.sleep(2)  # 等待加载完成
#
# mouse.left_button_click()
#
# # 8. F11全屏
# keyboard.fullscreen()
# time.sleep(2)

ser.close()  # 关闭串口
