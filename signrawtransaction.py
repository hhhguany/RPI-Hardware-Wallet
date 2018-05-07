# !/usr/bin/python2.7
# -*- coding: utf-8 -*-  
import pybitcointools
import serial
import time
from RPi import GPIO
from RPLCD.gpio import CharLCD

# 初始化 1602LCD 参数
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_rw=22, pin_e=35, pins_data=[40, 38, 36, 32, 33, 31, 29, 23], numbering_mode=GPIO.BOARD)
# 初始化串口参数
ser = serial.Serial("/dev/ttyAMA0", 9600)
# 初始化交易参数
scriptPubKey = "0100000001ef1c5dce011cc40479035d842f0d0f1cc79899f36f3c0318aa296efcb310c637010000006b4830450220706ec46ae2e4ed684cdf000f0c98bd9678bc015b2d5b88402e9a56f41a54145b022100fea3d188d8993ee4f2090a282c0db33d68212ad071c7b077c00841660ac5e76b012103edd2a055711f87e98d524e11c06512dd0e0c017aad1813483194573e2df2b882ffffffff01f6f1052a010000001976a9146dda16249cd864f4c16071f80f61d6acdaefd43f88ac00000000"
privKey = "7kNpxyfxTs6hsxWsqtUzWXhJhH1hEU2vMa3tsJ2r7mg144qtf52b"
# 交易 tx 范例
# tx = "0100000001ef1c5dce011cc40479035d842f0d0f1cc79899f36f3c0318aa296efcb310c6370100000000ffffffff01f6f1052a010000001976a9146dda16249cd864f4c16071f80f61d6acdaefd43f88ac00000000"

# 初始化 GPIO 参数
# GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

confirm_button = 13
shutdown_button = 11
GPIO.setup(confirm_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(shutdown_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 按键按下检测
def isPressed(pin):
    if GPIO.input(pin) == GPIO.HIGH:
        return True

# 屏幕重写
def lcd_new_print(string):
    lcd.clear()
    lcd.write_string(string)

# 主程序
def main():
    while True:
        lcd_new_print(u"Hardware Wallet Ready.")
        while isPressed(confirm_button):
            lcd_new_print(u"Holdon in 3 Second.")
            time.sleep(1)
            lcd_new_print(u"Holdon in 2 Second.")
            time.sleep(1)
            lcd_new_print(u"Holdon in 1 Second.")
            time.sleep(1)
            lcd_new_print(u"Serial Port Opened, Waitting...")

        serTx = ser.readline()
        # 处理串口来的信息，仅保留英文和数字
        # serTx=filter(str.isalnum, serTx)
        tx=filter(str.isalnum, serTx)
        
        # Debug Log
        # if serTx[:-1] == tx:
        #     print ok
        # else:
        #     print serTx + 'a'
        #     print tx + 'a'
        try:
            sigMsg = pybitcointools.smartsign(tx, privKey, scriptPubKey)
        except (ValueError, IndexError), e:
            lcd_new_print(u'Value Error')
        lcd_new_print(u'Send Ok..')

        ser.write(sigMsg)
        ser.flushInput()
        time.sleep(0.1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        if lcd != None:
            lcd_new_print("Hardware Wallet is stopped.")
        if ser != None:
            ser.close()