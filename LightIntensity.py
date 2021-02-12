# Amount of light reflected from Earth (intensity in lux), depending on air pollution
# https://www.epa.gov/pm-pollution/particulate-matter-pm-basics
#
# Luminance is a photometric measure of the luminous intensity per unit area of light travelling in a given direction.
# It describes the amount of light that passes through, is emitted from, or is reflected from a particular area,
# and falls within a given solid angle.
# reference: https://en.wikipedia.org/wiki/Luminance
#
# Relative luminance follows the photometric definition of luminance, but with the
# values normalized to 1 or 100 for a reference white. Like the photometric definition,
# it is related to the luminous flux density in a particular direction, which is radiant flux density
# weighted by the luminosity function y(λ) of the CIE Standard Observer.
# Y = 0.2126*R + 0.7152G + 0.0722B.
# reference: https://en.wikipedia.org/wiki/Relative_luminance

from PIL import Image  # Pillow library
import datetime

img = Image.open("test.jpg")
img = img.convert('RGB')

width = img.width
height = img.height

# creating copy, so it won't overwrite original picture
imgWater = img.copy().convert('HSV')
pixelsWater = imgWater.load()

# creating copy, so it won't overwrite original picture
imgClouds = img.copy()
pixelsClouds = imgClouds.load()

# creating copy, so it won't overwrite original picture
imgLand = img.copy()
pixelsLand = imgLand.load()

RelativeLuminance = 0

# AverageRelativeLuminance is responsible for average Relative Luminance of all picture, including window
AverageRelativeLuminance = 0

# AverageRelativeLuminance2 is responsible for average Relative Luminance of all picture, excluding window
AverageRelativeLuminance2 = 0

# auxiliary variable
AverageRelativeLuminance2pixels = 0

# Variables used for calculating average Luminance of water
WaterRelativeLuminance = 0
WaterPixels = 0
AverageWaterRelativeLuminance = 0

# Variables used for calculating average Luminance of clouds and snow
CloudsRelativeLuminance = 0
CloudsPixels = 0
AverageCloudsRelativeLuminance = 0

# Variables used for calculating average Luminance of Land
LandRelativeLuminance = 0
LandPixels = 0
AverageLandRelativeLuminance = 0

# Loop #1, responsible for:
# - calculating average Luminance of all picture
# - separating water form picture, using NDWI index

for X in range(0, width):  # image width
    for Y in range(0, height):  # image height

        # Original image pixels
        pixelRGB = img.getpixel((X, Y))  # Get pixel RGB values
        R, G, B = pixelRGB  # divide RBG into sigle variables

        # Calculates RelativeLuminance
        RelativeLuminance = (0.2126*R) + (0.7152*G) + (0.0722*B)
        RelativeLuminance = int(RelativeLuminance)
        AverageRelativeLuminance += RelativeLuminance

        # Calculates NDWI and casts it to 0-360 (so far so good)
        if(R+G) > 0:

            NDWI = (R - G) / (R + G)

            # cast from (-1,1) to (0,360)
            NDWI *= 130
            NDWI += 130

            if NDWI < 115:
                # ~via Zuzia
                pixelsWater[X, Y] = (int(NDWI), 200, 200)  # HSV
            else:
                pixelsWater[X, Y] = (0, 0, 0)

# converting to RGB, because I opened it in HSV earlier
imgWater = imgWater.convert('RGB')
pixelsWater = imgWater.load()

pixelsLand = imgLand.load()

# calculating average Luminance of whole picture, AverageRelativeLuminance divided by total pixels
AverageRelativeLuminance /= width*height

# Loop #2, responsible for:
# - calculating average Luminance of water + clouds + snow + land
# - separating water from the rest of the picture
# - separating window from the rest of the picture

for X in range(0, width):  # image width
    for Y in range(0, height):  # image height

        # Original image pixels
        pixelRGB = img.getpixel((X, Y))  # Get pixel RGB values
        R, G, B = pixelRGB  # divide RBG into sigle variables

        # Liczy RelativeLuminance
        RelativeLuminance = (0.2126 * R) + (0.7152 * G) + (0.0722 * B)
        RelativeLuminance = int(RelativeLuminance)

        # If Luminance of the pixel is less than average Luminance of whole picture, it is window

        if RelativeLuminance < (AverageRelativeLuminance / 3):
            pixelsLand[X, Y] = (0, 0, 0)
        else:
            # if pixels are not considered as window then average Luminance for the rest of the picture is calculated

            AverageRelativeLuminance2 += RelativeLuminance
            AverageRelativeLuminance2pixels += 1

        # imgWater opened in RGB
        pixelRGBWater = imgWater.getpixel((X, Y))  # Get pixel RGB values
        Rw, Gw, Bw = pixelRGBWater  # divide RBG into single variables

        # imgLand opened in RGB
        pixelRGBLand = imgLand.getpixel((X, Y))
        Rl, Gl, Bl = pixelRGBLand

        if Rl == 0 and Gl == 0 and Bl == 0:  # RGB values for land
            pixelsWater[X, Y] = (0, 0, 0)
            pixelsClouds[X, Y] = (0, 0, 0)  # erasing windows from picture with clouds

        elif Rw != 0 or Gw != 0 or Bw != 0:  # RGB values for water

            # Korzystając z okazji, wymazuję wodę ze zdjęć z chmurami i lądem ^_^
            pixelsLand[X, Y] = (0, 0, 0)
            pixelsClouds[X, Y] = (0, 0, 0)

            WaterRelativeLuminance += RelativeLuminance
            WaterPixels += 1

AverageRelativeLuminance2 /= AverageRelativeLuminance2pixels
print(AverageRelativeLuminance2)

if WaterPixels > 0:
    AverageWaterRelativeLuminance = WaterRelativeLuminance/WaterPixels

if CloudsPixels > 0:
    AverageCloudsRelativeLuminance = CloudsRelativeLuminance/CloudsPixels

if LandPixels > 0:
    AverageLandRelativeLuminance = LandRelativeLuminance / LandPixels

imageDatetime = datetime.datetime.now().strftime("%d.%m.%Y-%H:%M:%S")

data = open('LightIntensity.csv', 'w')
data.writelines("Datetime: ;"
                "AverageRelativeLuminance:  ;"
                "AverageRelativeLuminanceWithoutWindowBorders:    ;"
                "AverageWaterRelativeLuminance: \n")
data.write(str(imageDatetime)+';' +
           str(AverageRelativeLuminance) + ';' +
           str(AverageRelativeLuminance2)+';' +
           str(AverageWaterRelativeLuminance)+'\n')
data.close()

imgWater.save("_Water.jpg")
imgClouds.save("_Clouds.jpg")
imgLand.save("_Land.jpg")
