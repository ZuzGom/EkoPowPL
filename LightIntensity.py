"""
Amount of light reflected from Earth (intensity in lux), depending on air pollution
https://www.epa.gov/pm-pollution/particulate-matter-pm-basics

Luminance is a photometric measure of the luminous intensity per unit area of light travelling in a given direction.
It describes the amount of light that passes through, is emitted from, or is reflected from a particular area,
and falls within a given solid angle.
reference: https://en.wikipedia.org/wiki/Luminance

Relative luminance follows the photometric definition of luminance, but with the
values normalized to 1 or 100 for a reference white. Like the photometric definition,
it is related to the luminous flux density in a particular direction, which is radiant flux density
weighted by the luminosity function y(λ) of the CIE Standard Observer.
Y = 0.2126*R + 0.7152G + 0.0722B.
reference: https://en.wikipedia.org/wiki/Relative_luminance
"""

from PIL import Image
import datetime

def lightIntensity(name ,date):

    """
    Calculates Relative luminance for clouds and snow, water, land.
    Outputs data and saves it to '.csv' file. This data will be used for analysis on Earth.
    """

    img = Image.open(name)
    img = img.convert('RGB')

    width = img.width
    height = img.height

    # creating copy, so it won't overwrite original picture
    imgWater = img.copy().convert('HSV')
    pixelsWater = imgWater.load()

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

    """
    Loop #1, responsible for:
    - gathering information, which will be used for calculating average Luminance of all picture, including window
    - separating water form picture, using NDWI index
    """

    for X in range(0, width):  # image width
        for Y in range(0, height):  # image height

            # Original image pixels
            pixelRGB = img.getpixel((X, Y))  # Get pixel RGB values
            R, G, B = pixelRGB  # divide RBG into sigle variables

            # Calculates RelativeLuminance
            RelativeLuminance = (0.2126*R) + (0.7152*G) + (0.0722*B)
            RelativeLuminance = int(RelativeLuminance)
            AverageRelativeLuminance += RelativeLuminance

            # Calculates NDWI and casts it to 0-360
            if(R+G) > 0:
                NDWI = (R - G) / (R + G)

                # cast from (-1,1) to (0,360)
                NDWI *= 180
                NDWI += 180

                # marks water areas, makes everything else black
                if NDWI < 160:
                    # ~via Zuzia
                    pixelsWater[X, Y] = (int(NDWI), 200, 200)  # HSV
                else:
                    pixelsWater[X, Y] = (0, 0, 0)

    # converting to RGB, because I opened it in HSV earlier
    imgWater = imgWater.convert('RGB')
    pixelsWater = imgWater.load()

    # calculating average Luminance of whole picture, AverageRelativeLuminance divided by total pixels
    AverageRelativeLuminance /= width*height

    """
    # Loop #2, responsible for:
    # - gathering information, which will be used for calculating average Luminance of water + clouds and snow + land
    # - separating water from the rest of the picture
    # - separating window from the rest of the picture
    """

    for X in range(0, width):  # image width
        for Y in range(0, height):  # image height

            # Original image pixels
            pixelRGB = img.getpixel((X, Y))  # Get pixel RGB values
            R, G, B = pixelRGB  # divide RBG into sigle variables

            # Calculates RelativeLuminance
            RelativeLuminance = (0.2126 * R) + (0.7152 * G) + (0.0722 * B)
            RelativeLuminance = int(RelativeLuminance)

            # If Luminance of the pixel is less than average Luminance of whole picture divided by 3, it is window

            if RelativeLuminance < (AverageRelativeLuminance / 3):
                pixelsWater[X, Y] = (0, 0, 0)
            else:
                # if pixels are not considered as window then information
                # which will be used for calculating average Luminance for the rest of the picture is gathered
                AverageRelativeLuminance2 += RelativeLuminance
                AverageRelativeLuminance2pixels += 1



            # imgWater opened in RGB
            pixelRGBWater = imgWater.getpixel((X, Y))  # Get pixel RGB values
            Rw, Gw, Bw = pixelRGBWater  # divide RBG into single variables

            # RGB values for water, because in imgWater, other pixels but water are set to (0,0,0)
            if Rw != 0 or Gw != 0 or Bw != 0:
                WaterRelativeLuminance += RelativeLuminance
                WaterPixels += 1

            # separetes clouds and land, then gathers information used for calculating relative luminance for both of them
            if R>=200:
                CloudsRelativeLuminance += RelativeLuminance
                CloudsPixels += 1
            else:
                LandRelativeLuminance += RelativeLuminance
                LandPixels += 1

    # Calculating average relative luminance for: whole picture (excluding window), clouds + snow, water, land
    if AverageRelativeLuminance2pixels > 0:
        AverageRelativeLuminance2 /= AverageRelativeLuminance2pixels

    if WaterPixels > 0:
        AverageWaterRelativeLuminance =  WaterRelativeLuminance / WaterPixels


    if CloudsPixels > 0:
        AverageCloudsRelativeLuminance = CloudsRelativeLuminance /  CloudsPixels


    if LandPixels > 0:
        AverageLandRelativeLuminance = LandRelativeLuminance / LandPixels


    imageDatetime = datetime.datetime.now().strftime("%d.%m.%Y-%H:%M:%S")

    data = open('LightIntensity.csv', 'a')
    data.writelines("Datetime: ;"
                    "Date: ;"
                    "AverageRelativeLuminanceWithoutWindowBorders:    ;"
                    "AverageWaterRelativeLuminance: ;"
                    "AverageCloudsRelativeLuminance: ;"
                    "AverageLandRelativeLuminance \n")
    data.write(str(imageDatetime)+';' +
               str(date) + ';' +
               str(AverageRelativeLuminance2) + ';' +
               str(AverageWaterRelativeLuminance)+';' +
               str(AverageCloudsRelativeLuminance) + ';' +
               str(AverageLandRelativeLuminance)+'\n')
    data.close()
