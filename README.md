# CH9329KMS


##### 1.键盘输入
```python
import serial
from key_map import KeyBoard

ser = serial.Serial('COM3', 9600)  # 开启串口
keyboard = KeyBoard(ser=ser)
print(keyboard.send_data([KeyBoard.Key.Key_H]))  # 按下H
print(keyboard.release())  # 松开
print(keyboard.send_data([KeyBoard.Key.Key_E], ctrl=KeyBoard.Control.L_SHIFT))  # 按下大写E
print(keyboard.release())  # 松开
print(keyboard.send_data([KeyBoard.Key.Key_L]))  # 按下L
print(keyboard.release())  # 松开
print(keyboard.send_data([KeyBoard.Key.Key_L]))  # 按下L
print(keyboard.release())  # 松开
print(keyboard.send_data([KeyBoard.Key.Key_O]))  # 按下O
print(keyboard.release())  # 松开

ser.close()  # 关闭串口
```
##### 2.鼠标输入
```python
import serial

from mouse_map import Mouse

ser = serial.Serial('COM3', 9600)  # 开启串口
# 设置屏幕分辨率
mouse = Mouse(screen_width=2160, screen_height=1440, ser=ser)
# 移动绝对坐标
print(mouse.send_data_absolute(50, 50))
# 移动相对坐标(向右向下移动10个像素)屏幕左上角为坐标原点
print(mouse.send_data_relatively(10, 10))
# time.sleep(1)
# 双击鼠标左键
mouse.left_button_double_click()
# 关闭串口
ser.close()  
```