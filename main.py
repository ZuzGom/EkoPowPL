from time import sleep
from picamera import PiCamera
import ndvi
from PIL import Image

camera = PiCamera()
camera.resolution = (640, 480)
camera.start_preview()
# Camera warm-up time
sleep(2)
camera.capture("image.jpg")
#image = Image.open("2image.jpg")
#ndvi.index_convert(image)

#def capture_film():


def film_hd():
    camera.resolution = (1920, 1080)
    camera.framerate = 30
    camera.start_recording('video1.h264')
    camera.wait_recording(5)
    camera.stop_recording()


film_hd()

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
