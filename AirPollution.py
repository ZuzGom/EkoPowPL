#Amount of light reflected from Earth (intensity in lux), depending on air pollution

from PIL import Image #Pillow library
from math import sqrt
img = Image.open("test.jpg")
img = img.convert('RGB')

temp = img.copy()  # creating copy, so it won't overwrite original picture
pixels = temp.load()

def findWater():
    #water albedo 5-10%
    #NDWI=(G-IR)/(G+IR)

    NDWIsuma=0
    NDWI=0
    BrightnessSum = 0  # used for calculating average water brightness
    pixelCounter = 0  # counting water pixels
    for X in range(0, 1296): #image width
        for Y in range(0, 972): #image height
            pixelRGB = img.getpixel((X,Y)) # Get pixel RGB values
            R,G,B = pixelRGB #divide RBG into sigle variables

            if (G+R)!=0: #avoids division by zero
                NDWI=(G-R)/(G+R)
            else:
                NDWI=0


            #PL: Tutaj algorytm fajnie działa dla zaznaczania wody, ale zaznacza również fragmenty okna
            # dlatego zauważyłem że okno jest quite ciemne, wiec jak Brightness jest małe to można pominąć
            # zaznaczanie fragmentu okna, dzięki temu mi nie wydupi tego co chcę potem zrobić
            Brightness = sum([R, G, B]) / 3  ##0 is dark (black) and 255 is bright (white)
            if Brightness < 35:
                pixels[X,Y] = (0, 0, 0)
            else:
                #NDWIsuma = NDWI + NDWIsuma
                if NDWI > 0.05 and NDWI < 0.5: #NDWI > 0.05 works really great
                    pixels[X,Y] = (128, 234, 255)  #blue XD, visualization, so we can check how it works
                    BrightnessSum = BrightnessSum+Brightness
                    pixelCounter=pixelCounter+1
    return BrightnessSum,pixelCounter
    #NDWIsuma=NDWIsuma/(1296*972) #image size
    #print(NDWIsuma)


######################_MAIN_######################

BrightnessSum,pixelCounter=findWater()

if pixelCounter!=0:
    averageWaterBrightness=BrightnessSum/pixelCounter
else:
    print("BOOOOM!")

#AlbedoREL=B_unknown/B_reference
B_unknown=0 # PL:do policzenia
AlbedoREL=B_unknown/averageWaterBrightness
print(averageWaterBrightness)
print(AlbedoREL)

#AlbedoABS=0.08/AlbedoREL

AlbedoABS=0.18*AlbedoREL
print(AlbedoABS*100)

##################################################





temp.save("ProcessedL.jpg")  # saves picture