# Converting image to NDVI colored scale

# UWAGA! używam słów hsl i hsv wymiennie nie pomylcie się :3

from PIL import Image  # Pillow library
i = 4
# moje obrazy testowe są w formacie img1, img2... imgn więc...
# jesli chce prztestowac jeden z ich, to wpisuje jego liczbe i mam na wyjsciu ladnie zapisanie 1ndvi, 1hsl itd...
# reszta kometarzy po angieslku zeby nie bylo wam za latwo ;p

img = Image.open("imgtest\\img"+str(i)+".jpg")

# i get height and widith of image
w, h = img.size

out = img.copy().convert('HSV')  # creating hsv picture (h means color, i'll use it later)
img = img.convert('RGB')
temp = img.copy()  # creating copy, so it won't overwrite original picture

pixels = temp.load()  # i get pixel information of copied picture
pixels1 = out.load()  # and hsl one


def NDVIconvert():

    # checking every single pixel
    ndviSum = []  # list of every pixel's ndvi index

    for X in range(0, w):  # widith
        for Y in range(0, h):  # height
            pixelRGB = img.getpixel((X, Y))  # Get pixel's RGB values

            R, G, B = pixelRGB

            # ~via Kuba Frączek
            Brightness = sum(pixelRGB) / 3  # 0 is dark (black) and 255 is bright (white)

            if Brightness < 35:
                pixels[X, Y] = (0, 0, 0)  # shadows off
            else:
                if Brightness > 150:
                    pixels[X, Y] = (255, 255, 255)  # clouds off
                else:
                    if (R + B) != 0:  # avoids division by zero
                        NDVI = (R - B) / (R + B)
                    else:
                        NDVI = (R - B) / 1

                    ndviSum.append(NDVI)  # add index value to the list t.b.c.

                    # every value below 0 ends up as 0, water starts at about -0.1, so I add 0.15
                    NDVI = int((NDVI+0.15) * 500)  # then I multiply it by 500 to make a good contrast
                    # it cannot be float, because hsv and rgb can't read that ;c

                    pixels[X, Y] = (NDVI, NDVI, NDVI)  # one picture in GRAYSCALE
                    pixels1[X, Y] = (NDVI, 200, 200)
                    # and one picture in HSL, in which H is NDVI, so index value is one color of the scpectrum
                    # i figured it out by myself ngl

    avg = sum(ndviSum)/len(ndviSum)  # average ndvi value on the picture
    return avg, max(ndviSum)


# #####################_MAIN_######################

# I get average and maximum NDVI value
averageNDVI, maxi = NDVIconvert()
print(averageNDVI)
print(maxi)

# nie moge zapisac w formacie hsl ;c (hsv my mistake)
# zapisuje w moim formacie:

out.convert("RGB").save("testout\\"+str(i)+"hsl.jpg")  # saves picture in color scale
temp.save("testout\\"+str(i)+"ndvi.jpg")  # saves picture in grayscale
img.save("testout\\"+str(i)+"org.jpg")  # saves original picture to compare
