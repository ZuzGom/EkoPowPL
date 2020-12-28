# Converting image to NDVI colored scale

from PIL import Image  # Pillow library

i = 4
# moje obrazy testowe są w formacie img1, img2... imgn więc...
# jesli chce prztestowac jeden z ich, to wpisuje jest liczbe i mam na wyjsciu ladnie zapisanie 1ndvi, 1hsl itd...
# reszta kometarzy po angieslku zeby nie bylo wam za latwo ;p

img = Image.open("imgtest\\img" + str(i) + ".jpg")

# i get height and widith of image
w, h = img.size

out = img.copy().convert('HSV')  # creating hsv picture
img = img.convert('RGB')
temp = img.copy()  # creating copy, so it won't overwrite original picture

pixels = temp.load()
pixels1 = out.load()

print(img)


# cordinate = x, y = 150, 59
# using getpixel method
# print(temp.getpixel(cordinate))


def NDVIconvert():
    ndviSum = []

    for X in range(0, w):
        for Y in range(0, h):
            pixelRGB = img.getpixel((X, Y))  # Get pixel RGB values

            R, G, B = pixelRGB  # divide RBG into sigle variables

            Brightness = sum([R, G, B]) / 3  ##0 is dark (black) and 255 is bright (white)

            if Brightness < 35:
                pixels[X, Y] = (0, 0, 0)
            else:
                if Brightness > 150:
                    pixels[X, Y] = (255, 255, 255)
                else:
                    if (R + B) != 0:  # avoids division by zero
                        NDVI = (R - B) / (R + B)
                    else:
                        NDVI = (R - B) / 1
                    ndviSum.append(NDVI)
                    # every value below 0 ends up as 0, water starts at about -0.1, so I add 0.15
                    NDVI = int((NDVI + 0.15) * 500)  # then I multiply by 500 to make a good contrast

                    pixels[X, Y] = (NDVI, NDVI, NDVI)  # one picture in GRAYSCALE
                    pixels1[X, Y] = (NDVI, 200, 200)
                    # and one picture in HSL, in which H is NDVI, so index value is one color of the scpectrum

    avg = sum(ndviSum) / len(ndviSum)  # average ndvi value on the picture
    return avg, max(ndviSum)


######################_MAIN_######################

averageNDVI, maxi = NDVIconvert()
print(averageNDVI)
print(maxi)

temp.save("testout\\" + str(i) + "ndvi.jpg")  # saves original picture to compare
img.save("testout\\" + str(i) + "org.jpg")  # saves picture in grayscale
print(out.getpixel((250, 400)))

im2 = out.convert("RGB")  # nie moge zapisac w formacie hsl ;c (hsv my mistake)
im2.save("testout\\" + str(i) + "hsl.jpg")  # saves in color scale picture
