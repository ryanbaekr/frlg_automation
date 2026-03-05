import os
import random
import time

import serial
import cv2

"""
https://github.com/knflrpn/SwiCC_RP2040

Byte 0
0b00000000
    |||||\_ -
    ||||\__ +
    |||\___ LS
    ||\____ RS
    |\_____ HOME
    \______ CAPTURE

Byte 1
0b00000000
  |||||||\_ Y
  ||||||\__ B
  |||||\___ A
  ||||\____ X
  |||\_____ L
  ||\______ R
  |\_______ ZL
  \________ ZR

Byte 2
0x00 - Up
0x01 - Up/Right
0x02 - Right
0x03 - Down/Right
0x04 - Down
0x05 - Down/Left
0x06 - Left
0x07 - Up/Left
0x08 - Neutral
"""

template_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "zapdos.png")
template = cv2.imread(template_filepath)

method = cv2.TM_SQDIFF_NORMED

ser = serial.Serial("COM3", 115200)

# get the controller connected
for i in range(0, 3):
    # zr
    ser.write(bytearray("+IMM 008008 \n", "ascii"))
    time.sleep(0.3)
    # zl
    ser.write(bytearray("+IMM 004008 \n", "ascii"))
    time.sleep(0.3)

"""
expectations:
- not shiny:
  - 0.000000 < val < 0.000002
  - 1110, 45
- shiny:
  - 0.001000 < val
"""

count = 0

while True:
    # soft reset
    # a, b, x, y
    ser.write(bytearray("+IMM 000F08 \n", "ascii"))
    time.sleep(0.3)
    # neutral
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(3.3 + random.randint(0, 18)/120)  # confirmed

    # skip title sequence
    # a
    ser.write(bytearray("+IMM 000408 \n", "ascii"))
    time.sleep(0.3)
    # neutral
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(4.2 + random.randint(0, 18)/120)  # confirmed

    # press start
    # a
    ser.write(bytearray("+IMM 000408 \n", "ascii"))
    time.sleep(0.3)
    # neutral
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(2.7 + random.randint(0, 18)/120)  # confirmed

    # select save
    # a
    ser.write(bytearray("+IMM 000408 \n", "ascii"))
    time.sleep(0.3)
    # neutral
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(1.1 + random.randint(0, 18)/120)  # confirmed

    # skip recap
    # b
    ser.write(bytearray("+IMM 000208 \n", "ascii"))
    time.sleep(0.3)
    # neutral
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(2.0 + random.randint(0, 18)/120)  # confirmed

    # talk to zapdos
    # a
    ser.write(bytearray("+IMM 000408 \n", "ascii"))
    time.sleep(0.3)
    # neutral
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(1.3 + random.randint(0, 18)/120)  # confirmed

    # start battle
    # a
    ser.write(bytearray("+IMM 000408 \n", "ascii"))
    time.sleep(0.3)
    # neutral
    ser.write(bytearray("+IMM 000008 \n", "ascii"))
    time.sleep(4.9)  # confirmed

    cap = cv2.VideoCapture(1)  # default: 0

    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    ret, frame = cap.read()

    if not ret:
        break

    result = cv2.matchTemplate(frame, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    #cv2.imwrite("baseline.png", frame)
    cap.release()
    cv2.destroyAllWindows()

    print(min_val)
    print(min_loc)

    if min_val > 0.001:
        break

    count = count + 1
    print(count)
