# coding: utf-8
# program written by EkoPowPL Team from Jaslo (Poland) for
# AstroPi competition 2020/2021
# Team Members: Zuzanna Gomuła, Jakub Frączek, Jakub Batycki, Kamil Kras, Bartosz Królikowski, Wojciech Lupa
# Teachers: Wincenty Skwarek

import psutil
from time import sleep
from picamera import PiCamera
import datetime
import sys

import sHat
from kordy import isstrack
from ndvi import index_convert
from rgb import if_black


### funkcja sprawdzajaca czy zdjecie jest czarne gotowa (linia 41)

sHat.welcomeMessage()

sys.stdout = open('EkoPowPL.log', 'w')

path = sys.path
bytes_avail = psutil.disk_usage(path[0]).free
gigabytes_avail = bytes_avail / 1024 / 1024
for x in path:
    print(x)
print('Space left (MB): ')
print(gigabytes_avail)

now = datetime.datetime.now()
date = now.strftime("%m.%d_%H.%M.%S_")
lon, lat, country = isstrack()
date += str(lon) + '_' + str(lat) + '_' + country

camera = PiCamera()
camera.resolution = (1624, 1080)
camera.start_preview()
# Camera warm-up time
sleep(2)
sHat.camera()
name = 'image/'+date + '.jpg'
camera.capture(name)
if if_black(name):
    print('Noc')
    sHat.nightTime()
dane = index_convert(name)


def film_hd():
    sHat.camera()
    camera.resolution = (1624, 1080)
    camera.framerate = 30
    camera.start_recording('video/' + date + '.h264')
    camera.wait_recording(5)
    camera.stop_recording()
    camera.start_recording('video/lon' + date + '.h264')
    camera.wait_recording(60)
    camera.stop_recording()

# film_hd()


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
