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
