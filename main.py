from time import sleep
from picamera import PiCamera
import datetime
import sys

sys.stdout = open('EkoPowPL.log', 'w')

from kordy import isstrack
from ndvi import index_convert


now = datetime.datetime.now()
date = now.strftime("%m.%d_%H.%M.%S_")
lon, lat, country = isstrack()
date += str(lon) + '_' + str(lat) + '_' + country


camera = PiCamera()
camera.resolution = (640, 480)
camera.start_preview()
# Camera warm-up time
sleep(2)
name = 'image/ '+date + '.jpg'
camera.capture(name)
index_convert(name)


def film_hd():
    camera.resolution = (1920, 1080)
    camera.framerate = 30
    camera.start_recording('video' + date +'.h264')
    camera.wait_recording(5)
    camera.stop_recording()
    camera.start_recording('video' + date + '.h264')
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
path += "\comp"

try:
    os.makedirs(path)
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s" % path)
'''
