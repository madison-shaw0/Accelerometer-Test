import time
import board
import math
import digitalio
import busio
import storage
import sdcardio
import os
from adafruit_bus_device.i2c_device import I2CDevice
import i2c_lis3dh_AlexF
from i2c_lis3dh_AlexF import intConf
from i2c_lis3dh_AlexF import LIS3DH
from i2c_lis3dh_AlexF import LIS3DH_I2C


led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

#SD card init
spi= busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP12)
cs_sd=board.GP9
sdcard=sdcardio.SDCard(spi, cs_sd)
vfs = storage.VfsFat(sdcard)
#mount SD card's filesystem on CircuitPython filesystem
storage.mount(vfs, "/sd")
os.listdir('/sd')


#LIS3DH init
i2c=busio.I2C(board.GP15,board.GP14)
device=I2CDevice(i2c, 0x18)
int1= digitalio.DigitalInOut(board.GP13)
x= intConf()

#setting the threshold values
x.duration= 0x12  #0x03
x.threshold=6
x.drop= True

lis3dh= i2c_lis3dh_AlexF.LIS3DH_I2C(i2c, x, int1=int1)


#collects 30 data points when the device is turned on (25 Hz)
def collect():
    led.value=True
    with open("/sd/data.txt", "a") as f:
        f.write("\n"+ "\nNew Trial: \n")
    with open("/sd/data.txt", "a") as f:
        for i in range (50):
            x, y, z= lis3dh.acceleration
            f.write(("\n"+ str(x) + ", " + str(y) + ", " + str(z)+ ", "+ str(lis3dh.sensitivity))) #x, y, z, register reading, read 0x55 -> detects drop
            time.sleep(0.04) #sampling rate
    f.close()
    led.value=False


#Reading SD Card values & prints them in Shell
def read_sd():
    with open("/sd/data.txt", "r") as f:
        line = f.readline()
        while line != '':
            print(line)
            line = f.readline()

#Clears all values in SD card
def clear_sd():
    with open ("/sd/data.txt", "w") as f:
        f.write(" ")

#runs when device is powered on
#collect()
read_sd()
#clear_sd()
