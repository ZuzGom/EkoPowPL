# coding: utf-8
# program written by EkoPowPL Team from Jaslo (Poland) for
# AstroPi competition 2020/2021
# Team Members: Zuzanna Gomuła, Jakub Frączek, Jakub Batycki, Kamil Kras, Bartosz Królikowski, Wojciech Lupa
# Teachers: Wincenty Skwarek

import psutil
from time import sleep
from picamera import PiCamera
from datetime import datetime, timedelta
import sys
import os

from LightIntensity import lightIntensity
import sHat
from kordy import isstrack
from ndvi import index_convert
from rgb import if_black


# funkcja sprawdzajaca czy zdjecie jest czarne gotowa (linia 84)
# początek dużej pętli

sys.stdout = open('EkoPowPL.log', 'w')

start = datetime.now()

sHat.welcomeMessage()

path = sys.path
for x in path:
    print(x)

bytes_avail = psutil.disk_usage(path[0]).free
megabytes_avail = bytes_avail / 1024 / 1024
print('Space left (MB): ')
print(megabytes_avail)

camera = PiCamera()


def high_def(img):
    camera.resolution = (2048, 1536)
    camera.start_preview()
    # Camera warm-up time
    sleep(2)
    sHat.camera()
    camera.capture(img)


def low_def(img):
    camera.resolution = (480, 320)
    camera.start_preview()
    # Camera warm-up time
    sleep(2)
    sHat.camera()
    camera.capture(img)


def film_hd(s):
    sHat.camera()
    camera.resolution = (1080, 1080)
    camera.start_recording('video/' + date + '.h264')
    camera.wait_recording(s)
    camera.stop_recording()


last = datetime.now() - timedelta(minutes=5)

while True:
    now = datetime.now()
    if now > start + timedelta(minutes=165):
        break
    if now > last + timedelta(minutes=5):
        last = datetime.now()
        date = now.strftime("%m.%d_%H.%M.%S_")
        lon, lat, country = isstrack()
        date += str(int(lon)) + '_' + str(int(lat)) + '_' + country
        print(date)

        name = 'image/' + date + '.jpg'
        low = 'image/low_' + date + '.jpg'
        low_def(low)
        if not if_black(low):

            high_def(name)

            sHat.hourglass_s1()
            dane = index_convert(name)
            sHat.hourglass_s2()

            sHat.hourglass_s3()
            lightIntensity(name, date)
            sHat.hourglass_s4()

        else:
            os.remove(low)
            print('Noc')
            sHat.nightTime()

        # miejsce na zapisanie danych

# till the end less that 15 minutes left

bytes_avail = psutil.disk_usage(path[0]).free
megabytes_avail = bytes_avail / 1024 / 1024
print('Space left (MB): ')
print(megabytes_avail)

now = datetime.now()

if now < start + timedelta(minutes=168) and megabytes_avail > 300:
    film_hd(600)


sys.stdout.close()

'''
# creating output folder
import os

path = os.getcwd()
print ("The current working directory is %s" % path)
# define the name of the directory to be created
path += "\\comp"

try:
    os.makedirs(path)
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s" % path)
'''
