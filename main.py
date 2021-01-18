from time import sleep
from picamera import PiCamera
import ndvi

camera = PiCamera()
camera.resolution = (1296,972)
camera.start_preview()
# Camera warm-up time
sleep(2)
camera.capture("image.jpg")
#ndvi.index_convert("image.jpg")
