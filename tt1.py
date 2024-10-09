import serial

from mouse_map import Mouse

ser = serial.Serial('COM3', 9600)  # 开启串口
# key_board = KeyBoard(ser)
# key_board.send_data([KeyBoard.KeyDataMap.A, KeyBoard.KeyDataMap.S, KeyBoard.KeyDataMap.D])
# key_board.release()
mouse = Mouse(screen_width=2160, screen_height=1440, ser=ser)
print(mouse.send_data_absolute(50, 50))
print(mouse.send_data_relatively(10, 10))
# time.sleep(1)
mouse.left_button_double_click()
# mouse.send_data_relatively(10, 10)
# index = 0
# while True:
#     if index > 500:
#         break
#     index += 1
#     time.sleep(0.05)
#     logger.info(mouse.send_data_relatively(10, 10))
# print(mouse.left_button_click())
# reset(ser)

ser.close()  # 关闭串口
