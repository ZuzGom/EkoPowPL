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

from LightIntensity import lightIntensity
import sHat
from kordy import isstrack
from ndvi import index_convert
from rgb import if_black


### funkcja sprawdzajaca czy zdjecie jest czarne gotowa (linia 41)

sHat.welcomeMessage()

sys.stdout = open('EkoPowPL.log', 'w')

path = sys.path
bytes_avail = psutil.disk_usage(path[0]).free
megabytes_avail = bytes_avail / 1024 / 1024
for x in path:
    print(x)
print('Space left (MB): ')
print(megabytes_avail)

now = datetime.datetime.now()
date = now.strftime("%m.%d_%H.%M.%S_")
lon, lat, country = isstrack()
date += str(int(lon)) + '_' + str(int(lat)) + '_' + country

camera = PiCamera()
camera.resolution = (2048,1536)
camera.start_preview()
# Camera warm-up time
sleep(2)
sHat.camera()
name = 'image/'+date + '.jpg'
camera.capture(name)
if if_black(name):
    print('Noc')
    sHat.nightTime()
sHat.hourglass_s1()
dane = index_convert(name)
sHat.hourglass_s2()

sHat.hourglass_s3()
lightIntensity(name, date)
sHat.hourglass_s4()


def film_hd(s):
    sHat.camera()
    camera.resolution = (1920, 1080)
    camera.start_recording('video/' + date + '.h264')
    camera.wait_recording(s)
    camera.stop_recording()

# film_hd(5)


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
