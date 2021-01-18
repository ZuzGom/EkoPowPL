from time import sleep
from picamera import PiCamera
import ndvi
from PIL import Image, ImageDraw, ImageFont



camera = PiCamera()
camera.resolution = (1296,972)
camera.start_preview()
# Camera warm-up time
sleep(2)
camera.capture("image.jpg")
image = Image.open("image.jpg")
ndvi.index_convert(image)
