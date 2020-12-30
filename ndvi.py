# Converting image to NDVI colored scale

# UWAGA! używam słów hsl i hsv wymiennie nie pomylcie się :3

from PIL import Image, ImageDraw, ImageFont  # Pillow library
i = 14
# moje obrazy testowe są w formacie img1, img2... imgn więc...
# jesli chce prztestowac jeden z nich, to wpisuje jego liczbe i mam na wyjsciu ladnie zapisanie 1ndvi, 1hsl itd...
# reszta kometarzy po angieslku zeby nie bylo wam za latwo ;p

img = Image.open("imgtest\\img"+str(i)+".jpg")

# I get height and widith of image
w, h = img.size

out = img.copy().convert('HSV')  # creating hsv picture (h means color, i'll use it later)
img = img.convert('RGB')
temp = img.copy()  # creating copy, so it won't overwrite original picture

pixels = temp.load()  # I get pixel information of copied picture
pixels1 = out.load()  # and hsl one


def con(x):
    # every value below 0 ends up as 0, water starts at about -0.1, so I add 0.15
    # then I multiply it by 500 to make a good contrast
    # it cannot be float, because hsv and rgb can't read that ;c
    return int((x+0.15) * 500)


def NDVIconvert():

    # checking every single pixel
    ndviSum = []  # list of every pixel's ndvi index

    for X in range(0, w):  # widith
        for Y in range(0, h):  # height
            pixelRGB = img.getpixel((X, Y))  # Get pixel's RGB values

            r, g, b = pixelRGB

            # ~via Kuba Frączek
            Brightness = sum(pixelRGB) / 3  # 0 is dark (black) and 255 is bright (white)

            if Brightness < 35:
                pixels[X, Y] = (0, 0, 0)  # shadows off
            else:
                if Brightness > 180:
                    pixels[X, Y] = (255, 255, 255)  # clouds off
                else:
                    if (r + b) != 0:  # avoids division by zero
                        NDVI = (r - b) / (r + b)
                    else:
                        NDVI = (r - b) / 1

                    ndviSum.append(NDVI)  # add index value to the list t.b.c.

                    NDVI = con(NDVI)

                    pixels[X, Y] = (NDVI, NDVI, NDVI)  # one picture in GRAYSCALE
                    pixels1[X, Y] = (NDVI, 200, 200)
                    # and one picture in HSL, in which H is NDVI, so index value is one color of the scpectrum
                    # i figured it out by myself ngl
    print('gon')
    # ####### skala ######

    s = int((h-100)/200)  # skala skali (sprawdzam ile razy w h miesci sie dlugosc skali)
    if s > 1:
        s -= 1  # zmiejszam i tak

    font = ImageFont.truetype("arial.ttf", 2+s*10)

    # creating scale bar
    for x in range(w-10 - s*10, w-10):
        n = -0.2
        for y in range(100, s*200+100):
            nv = con(n)  # the same contrast as at picture
            pixels[x, y] = (nv, nv, nv)
            pixels1[x, y] = (nv, 200, 200)
            if n>0.4:
                pixels1[x - s * 30, y] = (nv, 200, 200)
            n += 0.003/s

    ss = 32 * s  # odstępy między numerami
    hh = 100 - 2  # początek skali

    # scale text on the hsv picture
    zo = ImageDraw.Draw(out)
    zo.text((w - 13 - s * 30, hh),            "-.2",   (0, 0, 200), font=font)
    zo.text((w - 13 - s * 30, hh + 1 * ss),   "-.1",   (0, 0, 200), font=font)
    zo.text((w - 3 - s * 30, hh + 2 * ss),    "0",     (0, 0, 200), font=font)
    zo.text((w - 7 - s * 30, hh + 3 * ss),    ".1",    (0, 0, 200), font=font)
    zo.text((w - 7 - s * 30, hh + 4 * ss),    ".2",    (0, 0, 200), font=font)
    zo.text((w - 7 - s * 30, hh + 5 * ss),    ".3",    (0, 0, 200), font=font)
    zo.text((w - 7 - s * 30, hh + 6 * ss),    ".4",    (0, 0, 200), font=font)

    # scale on the grayscale picture
    za = ImageDraw.Draw(temp)
    za.text((w - 13 - s * 30, hh),            "-.2",   (255, 255, 255), font=font)
    za.text((w - 13 - s * 30, hh + 1 * ss),   "-.1",   (255, 255, 255), font=font)
    za.text((w - 3 - s * 30, hh + 2 * ss),    "0",     (255, 255, 255), font=font)
    za.text((w - 7 - s * 30, hh + 3 * ss),    ".1",    (255, 255, 255), font=font)
    za.text((w - 7 - s * 30, hh + 4 * ss),    ".2",    (255, 255, 255), font=font)
    za.text((w - 7 - s * 30, hh + 5 * ss),    ".3",    (255, 255, 255), font=font)
    za.text((w - 7 - s * 30, hh + 6 * ss),    ".4",    (255, 255, 255), font=font)


    avg = sum(ndviSum)/len(ndviSum)  # average ndvi value on the picture
    print(min(ndviSum))
    return avg, max(ndviSum)


# #####################_MAIN_######################

# I get average and maximum NDVI value
averageNDVI, maxi = NDVIconvert()
print(averageNDVI)
print(maxi)

# nie moge zapisac w formacie hsl ;c (hsv my mistake)
# zapisuje w moim formacie:

out.convert("RGB").save("testout\\"+str(i)+"_hsl.jpg")  # saves picture in color scale
temp.save("testout\\"+str(i)+"_ndvi.jpg")  # saves picture in grayscale
img.save("testout\\"+str(i)+"_org.jpg")  # saves original picture to compare
