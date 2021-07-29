from machine import UART
import machine
import os
print("Hello boot")
uart = UART(0, baudrate=115200)
os.dupterm(uart)

machine.main('main.py')