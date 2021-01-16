# Amount of light reflected from Earth (intensity in lux), depending on air pollution
# https://www.epa.gov/pm-pollution/particulate-matter-pm-basics
#
# Illuminance - natężenie oświetlenia to całkowity strumień świetlny padający na powierzchnię na jednostkę powierzchni,
# jest to miara tego, jak bardzo padające światło oświetla powierzchnię. Mierzone w LUX-ach
#
# Luminance is a photometric measure of the luminous intensity per unit area of light travelling in a given direction.
# It describes the amount of light that passes through, is emitted from, or is reflected from a particular area,
# and falls within a given solid angle.
# PL: Luminancja to fotometryczna miara natężenia światła na jednostkę
# powierzchni światła przemieszczającego się w danym kierunku.
# # Opisuje ilość światła, które przechodzi, jest emitowane lub odbijane
# od określonego obszaru i pada pod określonym kątem bryłowym.
# reference: https://en.wikipedia.org/wiki/Luminance
#
# Relative luminance follows the photometric definition of luminance, but with the
# values normalized to 1 or 100 for a reference white. Like the photometric definition,
# it is related to the luminous flux density in a particular direction, which is radiant flux density
# weighted by the luminosity function y(λ) of the CIE Standard Observer.
# PL: Luminancja względna jest zgodna z definicją fotometryczną luminancji, ale z wartościami
# znormalizowanymi do 1 lub 100 dla bieli odniesienia. Podobnie jak definicja fotometryczna,
# jest ona związana z gęstością strumienia świetlnego w określonym kierunku, którym jest gęstość
# strumienia promieniowania ważone funkcją jasności y (λ) CIE Standard Observer.
# Y = 0.2126*R + 0.7152G + 0.0722B.
# reference: https://en.wikipedia.org/wiki/Relative_luminance
#
# Założenie tego co chcę zrobić jest takie: policzę luminancję dla  całych zdjęć,
# osobno dla wody, chmur i śniegu oraz lądu(jeśli się uda)
# potem nałożenie na mapę zanieczyszczeń i szukanie związku xd (powodzenia ja)
#
# Oblicznie luminancji dla całego zdjęcia: T
# Oblicznie luminancji dla wody: T
# Oblicznie luminancji dla chmur i śniegu: N
# Oblicznie luminancji dla lądu: N
#
# TO DO:
# - odróżnić chmury od lądu i obliczyć ich średnią luminancję

from PIL import Image  # Pillow library
import datetime


img = Image.open("test.jpg")
img = img.convert('RGB')

# Robię kopię dla kolejno Wody, Chmur i Lądu żeby móc sobie zobrazować czy algorytm dobrze działa

width = 1296
height = 972

# width = 1920
# height = 1080

imgWater = img.copy().convert('HSV')  # creating copy, so it won't overwrite original picture
pixelsWater = imgWater.load()

imgClouds = img.copy()  # creating copy, so it won't overwrite original picture
pixelsClouds = imgClouds.load()

imgLand = img.copy()  # creating copy, so it won't overwrite original picture
pixelsLand = imgLand.load()

# Formuła na względną luminancję: Y = 0.2126*R + 0.7152*G + 0.0722*B
RelativeLuminance = 0

# AverageRelativeLuminance odpowiada za średnią luminancję całego zdjęcia, włącznie z oknem
AverageRelativeLuminance = 0

# AverageRelativeLuminance2 odpowiada za średnią luminancję zdjęcia bez okna
AverageRelativeLuminance2 = 0
AverageRelativeLuminance2pixels = 0  # zmienna pomocnicza

# Obliczanie średniej luminancji dla wody
WaterRelativeLuminance = 0
WaterPixels = 0
AverageWaterRelativeLuminance = 0

# Obliczanie średniej luminancji dla chmur
CloudsRelativeLuminance = 0
CloudsPixels = 0
AverageCloudsRelativeLuminance = 0

# Obliczanie średniej luminancji dla lądu
LandRelativeLuminance = 0
LandPixels = 0
AverageLandRelativeLuminance = 0

# Pętla #1, odpowiedzialna za:
# - policzenie średniej luminancji całego zdjęcia
# - wyodrębnienie wody ze zdjęcia za pomocą indeksu NDWI

for X in range(0, width):  # image width
    for Y in range(0, height):  # image height

        # Original image pixels
        pixelRGB = img.getpixel((X, Y))  # Get pixel RGB values
        R, G, B = pixelRGB  # divide RBG into sigle variables

        # Liczy RelativeLuminance
        RelativeLuminance = (0.2126*R) + (0.7152*G) + (0.0722*B)
        RelativeLuminance = int(RelativeLuminance)
        AverageRelativeLuminance += RelativeLuminance

        # Obliczenie NDWI i zrzutowanie do 0-360 (tak mi się wydaje, tak chciałem żeby działało, so far so good)
        if(R+G) > 0:

            NDWI = (R - G) / (R + G)

            # Rzutowanie (-1,1) do (0,360)
            NDWI *= 130
            NDWI += 130

            # Nie mogę tu policzyć średniej luminancji bo zaznaczane są fragmenty okna,
            # pozbedę się ich w następnej pętli

            if NDWI < 115:  # Na oko, so far so good
                # ~via Zuzia
                pixelsWater[X, Y] = (int(NDWI), 200, 200)  # HSV
            else:
                pixelsWater[X, Y] = (0, 0, 0)


imgWater = imgWater.convert('RGB')  # konwertuje do rgb, bo wcześniej otworzyłem w hsv
pixelsWater = imgWater.load()

pixelsLand = imgLand.load()

# wyliczanie średniej luminancji całego zdjęcia, AverageRelativeLuminance podzielone przez liczbę pikseli
AverageRelativeLuminance /= width*height

# Pętla #2, odpowiedzialna za:
# - Obliczenie średniej luminancji dla wody + chmur i śniegu + lądu
# - Obliczenie średniej luminancji dla wody
# - wyodręgnienie wody ze zdjęcia z chmurami i lądem
# - wyodrębnienie okna ze zdjęcia z chmurami i lądem

for X in range(0, width):  # image width
    for Y in range(0, height):  # image height

        # Original image pixels
        pixelRGB = img.getpixel((X, Y))  # Get pixel RGB values
        R, G, B = pixelRGB  # divide RBG into sigle variables

        # Liczy RelativeLuminance
        RelativeLuminance = (0.2126 * R) + (0.7152 * G) + (0.0722 * B)
        RelativeLuminance = int(RelativeLuminance)

        # pozbywa się tego okna??? przynajmniej na tych przykładowych zdjęciach które mam
        # wpadłem na coś takiego i na różnych zdjęciach które testuje, działa całkiem spoko
        # Czyli jeżeli luminancja danego piksela jest mniejsza od średniej luminancji całego zdjęcia/3 to jest oknem :p

        if RelativeLuminance < (AverageRelativeLuminance / 3):
            pixelsLand[X, Y] = (0, 0, 0)
        else:

            # jeżeli piksele nie są "oknem" to jest liczona średnia luminancja dla reszty zdjęcia: wody + chmur + lądu

            AverageRelativeLuminance2 += RelativeLuminance
            AverageRelativeLuminance2pixels += 1

        # imgWater otwarty w RGB
        pixelRGBWater = imgWater.getpixel((X, Y))  # Get pixel RGB values
        Rw, Gw, Bw = pixelRGBWater  # divide RBG into sigle variables

        # imgLand otwarty w RGB
        pixelRGBLand = imgLand.getpixel((X, Y))
        Rl, Gl, Bl = pixelRGBLand

        # Ustawiam czarny na zdjeciu z woda tam gdzie wczesniej ustawiłem czarny na zdjeciu z lądem xd
        # chodzi o to zeby sie pozbyc okna
        if Rl == 0 and Gl == 0 and Bl == 0:  # wartości RGB dla lądu
            pixelsWater[X, Y] = (0, 0, 0)
            pixelsClouds[X, Y] = (0, 0, 0)  # przy okazji usuwam okno ze zdjęcia z chmurami

        elif Rw != 0 or Gw != 0 or Bw != 0:  # wartości RGB dla wody

            # Korzystając z okazji, wymazuję wodę ze zdjęć z chmurami i lądem ^_^
            pixelsLand[X, Y] = (0, 0, 0)
            pixelsClouds[X, Y] = (0, 0, 0)

            # W tym momencie okno jest czarne, oraz we wcześniejszej pętli inne piksele niż woda ustawiłem na 0,0,0
            # zatem jedynymi pikselami różnymi od 0,0,0 powinna być woda
            # dlatewgo liczę tutaj jej średnią luminancję

            WaterRelativeLuminance += RelativeLuminance
            WaterPixels += 1
        """
        # Obliczam NDWI, żeby sprawdzić Relative Luminance dla samej wody
        NDWI=0
        if (G + R)>0:
            NDWI = (G - R) / (G + R)

        if(NDWI)>0.05:
            pixelsWater[X,Y]=(R,G,B)
            WaterRelativeLuminance+=RelativeLuminance
            WaterPixels+=1
        else:
            pixelsWater[X,Y] = (0, 0, 0)

        # Tristimulus values X= −0.14282×R+1.54924×G−0.95641×B
        # Tristimulus values Y= −0.32466×R+1.57837×G−0.73191×B
        # Tristimulus values Z= −0.68202×R+0.77073×G−0.56332×B
        # Chromaticity x=X / (X+Y+Z)
        # Chromaticity y=Y / (X+Y+Z)
        # SWR(%)= −256.321×x+103.9395×y+63.55018
        # CCT= 149.66×SWR+2134

        tvX= (-0.14282*R)+(1.54924*G)-(0.95641*B)
        tvY= (-0.32466*R)+(1.57837*G)-(0.73191*B)
        tvZ= (-0.68202*R)+(0.77073*G)-(0.56332*B)

        chX=0
        chY=0
        if (tvX+tvY+tvZ) > 0:
            chX= tvX / (tvX+tvY+tvZ)
            chY= tvY / (tvX+tvY+tvZ)

        SWR= (-256.321*chX) + (103.9395*chY) + 63.55018
        CCT = (149.66*SWR) + 2134
        CCT=abs(CCT)

        #clouds

        #if abs(R-B)<25 and abs(R-G)<25 and abs(B-R)<25 and abs(B-G)<25 and abs(G-R)<25 and abs(G-B)<25:
        if (NDWI)>0.05:
            pixelsClouds[X, Y] = (0, 0, 0)
        #elif (R-Brig+G-Brig+B-Brig)>0 and Brig - RelativeLuminance > 0:
        elif R-B==0 and B-G==0:
            pixelsClouds[X, Y] = (R, G, B)
            CloudsRelativeLuminance+=RelativeLuminance
            CloudsPixels+=1
        else:
            pixelsClouds[X, Y] = (0, 0, 0)

        #land
        if (NDWI)>0.05:
            pixelsLand[X, Y] = (0, 0, 0)
        #elif (R-Brig+G-Brig+B-Brig)>0 and Brig - RelativeLuminance > 0:
        elif Brightness > 60 and abs(R-B)<25 and abs(R-G)<25 and abs(B-R)<25 
        # and abs(B-G)<25 and abs(G-R)<25 and abs(G-B)<25:
            pixelsLand[X, Y] = (0, 0, 0)
        elif Brightness < 60:
            pixelsLand[X, Y] = (0, 0, 0)
        else:
            pixelsLand[X, Y] = (R, G, B)
            LandRelativeLuminance += RelativeLuminance
            LandPixels += 1
        """

AverageRelativeLuminance2 /= AverageRelativeLuminance2pixels
print(AverageRelativeLuminance2)

if WaterPixels > 0:
    AverageWaterRelativeLuminance = WaterRelativeLuminance/WaterPixels

if CloudsPixels > 0:
    AverageCloudsRelativeLuminance = CloudsRelativeLuminance/CloudsPixels

if LandPixels > 0:
    AverageLandRelativeLuminance = LandRelativeLuminance / LandPixels

imageDatetime = datetime.datetime.now().strftime("%d.%m.%Y-%H:%M:%S")

data = open('LightIntensity.csv', 'a')
dane = ["Datetime: "+str(imageDatetime)]
dane += [";   AverageRelativeLuminance: "+str(AverageRelativeLuminance)]
dane += [";  AverageRelativeLuminanceWithoutWindowBorders: "+str(AverageRelativeLuminance2)]
dane += [";    AverageWaterRelativeLuminance: "+str(AverageWaterRelativeLuminance)]
dane += ['\n']
data.writelines(str(dane))
data.close()


# imgWater = imgWater.convert('RGB')

imgWater.save("_Water.jpg")
imgClouds.save("_Clouds.jpg")
imgLand.save("_Land.jpg")
