from time import sleep
# from picamera import PiCamera

from PIL import Image
import glob
from kordy import isstrack
import ndvi
import datetime

now = datetime.datetime.now()
date = now.strftime("%D_%H.%M.%S_")
lon, lat = isstrack()
date += str(lon) + '_' + str(lat)

camera = PiCamera()
camera.resolution = (640, 480)
camera.start_preview()
# Camera warm-up time
sleep(2)
camera.capture("image\\"+date + ".jpg")


for infile in glob.glob("image\\*.jpg"):
    image = Image.open(date + ".jpg")
    ndvi.index_convert(image)


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
'''


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
