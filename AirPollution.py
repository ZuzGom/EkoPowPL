#Amount of light reflected from Earth (intensity in lux), depending on air pollution

from PIL import Image #Pillow library
from math import sqrt
img = Image.open("test.jpg")
img = img.convert ('RGB')

def imageBrightness(): # converts image into Grayscale
    temp = img.copy()  # creating copy, so it won't overwrite original picture
    for X in range(0, 1296): #image width
        for Y in range(0, 972): #image height
            pixelRGB = img.getpixel((X,Y)) # Get pixel RGB values
            R,G,B = pixelRGB #divide RBG into sigle variables
            Brightness = sum([R,G,B])/3 ##0 is dark (black) and 255 is bright (white)
            #print("B",Brightness)
            pixelRGB = int(Brightness),int(Brightness),int(Brightness) #set all: R,G,B to the same value to get Grayscale
            temp.putpixel((X,Y),pixelRGB) #Set Pixels
    temp.save("Processed.jpg") #saves picture

def imageLuminanceA(): # converts image into Grayscale
    temp = img.copy()  # creating copy, so it won't overwrite original picture
    for X in range(0, 1296): #image width
        for Y in range(0, 972): #image height
            pixelRGB = img.getpixel((X,Y)) # Get pixel RGB values
            R,G,B = pixelRGB #divide RBG into sigle variables
            LuminanceA = (0.2126*R) + (0.7152*G) + (0.0722*B)
            #print("L",LuminanceA)
            pixelRGB = int(LuminanceA),int(LuminanceA),int(LuminanceA) #set all: R,G,B to the same value to get Grayscale
            temp.putpixel((X,Y),pixelRGB) #Set Pixels
    temp.save("ProcessedL.jpg") #saves picture


imageLuminanceA()
imageBrightness()