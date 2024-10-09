import serial
from key_map import KeyBoard

ser = serial.Serial('COM3', 9600)  # 开启串口

keyboard = KeyBoard(ser=ser)
print(keyboard.send_data([KeyBoard.KeyDataMap.H]))  # 按下H
print(keyboard.release())  # 松开
print(keyboard.send_data([KeyBoard.KeyDataMap.E], ctrl=KeyBoard.ControlButtonMap.L_SHIFT))  # 按下大写E
print(keyboard.release())  # 松开
print(keyboard.send_data([KeyBoard.KeyDataMap.L]))  # 按下L
print(keyboard.release())  # 松开
print(keyboard.send_data([KeyBoard.KeyDataMap.L]))  # 按下L
print(keyboard.release())  # 松开
print(keyboard.send_data([KeyBoard.KeyDataMap.O]))  # 按下O
print(keyboard.release())  # 松开

ser.close()  # 关闭串口
