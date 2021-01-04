# Converting image to NDVI colored scale

# UWAGA! używam słów hsl i hsv wymiennie nie pomylcie się :3

from PIL import Image, ImageDraw, ImageFont  # Pillow library
import matplotlib.pyplot as plt

def NDVIconvert(img):

    # I get height and widith of image
    w, h = img.size

    def operation(code, img):
        index_col = img.copy().convert('HSV')  # creating hsv picture (h means color, i'll use it later)


        img_rgb = img.convert('RGB')
        index_bw = img_rgb.copy()  # creating copy, so it won't overwrite original picture

        px_index_bw = index_bw.load()  # I get pixel information of copied picture
        px_index_col = index_col.load()  # and hsl one

        # checking every single pixel
        indexSum = []  # list of every pixel's index index

        def con(v):  # contrast function
            # every value below 0 ends up as 0, water starts at about -0.1, so I add 0.15
            # then I multiply it by 500 to make a good contrast
            # it cannot be float, because hsv and rgb can't read that ;c
            return int((v + 0.2) * 400)

        for X in range(0, w):  # widith
            for Y in range(0, h):  # height
                pixelRGB = img_rgb.getpixel((X, Y))  # Get pixel's RGB values

                r, g, b = pixelRGB

                # ~via Kuba Frączek
                Brightness = sum(pixelRGB) / 3  # 0 is dark (black) and 255 is bright (white)

                if Brightness < 35:
                    px_index_bw[X, Y] = (0, 0, 0)  # shadows off
                else:
                    if Brightness > 200:
                        px_index_bw[X, Y] = (255, 255, 255)  # clouds off
                    else:

                        index = code(r, g, b)
                        indexSum.append(index)  # add index value to the list t.b.c.

                        index = con(index)  # a nice contrast

                        px_index_bw[X, Y] = (index, index, index)  # one picture in GRAYSCALE
                        px_index_col[X, Y] = (index, 200, 200)
                        # and one picture in HSL, in which H is index, so index value is one color of the scpectrum
                        # i figured it out by myself ngl


        print('zdjęcie nr. ' + str(i))
        # ####### skala ######

        s = int((h - 100) / 200)  # skala skali (sprawdzam ile razy w h miesci sie dlugosc skali)
        if s > 1:
            s -= 1  # zmiejszam i tak

        font = ImageFont.truetype("arial.ttf", 2 + s * 10)

        def skala(im_b, px_b, im_c, px_c):
            for x in range(w - 10 - s * 10, w - 10):
                n = -0.2
                for y in range(100, s * 200 + 100):
                    nv = con(n)  # the same contrast as at picture
                    px_b[x, y] = (nv, nv, nv)
                    px_c[x, y] = (nv, 200, 200)
                    n += 0.003 / s

            ss = 32 * s  # odstępy między numerami
            hh = 100 - 2  # początek skali

            # scale text on the hsv picture
            zo = ImageDraw.Draw(im_c)
            zo.text((w - 13 - s * 30, hh), "-.2", (0, 0, 200), font=font)
            zo.text((w - 13 - s * 30, hh + 1 * ss), "-.1", (0, 0, 200), font=font)
            zo.text((w - 3 - s * 30, hh + 2 * ss), "0", (0, 0, 200), font=font)
            zo.text((w - 7 - s * 30, hh + 3 * ss), ".1", (0, 0, 200), font=font)
            zo.text((w - 7 - s * 30, hh + 4 * ss), ".2", (0, 0, 200), font=font)
            zo.text((w - 7 - s * 30, hh + 5 * ss), ".3", (0, 0, 200), font=font)
            zo.text((w - 7 - s * 30, hh + 6 * ss), ".4", (0, 0, 200), font=font)

            # scale on the grayscale picture
            za = ImageDraw.Draw(im_b)
            za.text((w - 13 - s * 30, hh), "-.2", (255, 255, 255), font=font)
            za.text((w - 13 - s * 30, hh + 1 * ss), "-.1", (255, 255, 255), font=font)
            za.text((w - 3 - s * 30, hh + 2 * ss), "0", (255, 255, 255), font=font)
            za.text((w - 7 - s * 30, hh + 3 * ss), ".1", (255, 255, 255), font=font)
            za.text((w - 7 - s * 30, hh + 4 * ss), ".2", (255, 255, 255), font=font)
            za.text((w - 7 - s * 30, hh + 5 * ss), ".3", (255, 255, 255), font=font)
            za.text((w - 7 - s * 30, hh + 6 * ss), ".4", (255, 255, 255), font=font)

            '''
            what scale does:
            - fits to any picture above 300 px height
            - change its value according to contrast on the picture
            - ...
            '''

        skala(index_bw, px_index_bw, index_col, px_index_col)
        return index_bw, index_col


    def ndvi(r,g,b):
        if (r + b) != 0:  # avoids division by zero
            ix = (r - b) / (r + b)
        else:
            ix = (r - b) / 1
        return ix

    def ndwi(r,g,b):
        if (r + g) != 0:  # avoids division by zero
            ix = (r - g) / (r + g)
        else:
            ix = (r - g) / 1
        return ix

    ndvi_bw, ndvi_col = operation(ndvi, img)
    ndwi_bw, ndwi_col = operation(ndwi, img)

    # creating scale bar



    return ndvi_bw, ndvi_col, ndwi_bw, ndwi_col


# #####################_MAIN_######################

# moje obrazy testowe są w formacie img1, img2... imgn więc...
# jesli chce przetestowac jeden z nich, to wpisuje jego liczbe i mam na wyjsciu ladnie zapisanie 1_ndvi, 1_hsl itd...
# reszta kometarzy po angielsku zeby nie bylo wam za latwo ;p

for x in range(14, 15):
    i = 3

    image = Image.open("imgtest\\img" + str(i) + ".jpg")

    # I get average and maximum NDVI value, ndvi pic and color pic
    ndvi_bw, ndvi_col, ndwi_bw, ndwi_col = NDVIconvert(image)
    # I changed it, so NDVIconvert is separated function, which can be called on any picture

    # nie moge zapisac w formacie hsl ;c (hsv my mistake)
    # zapisuje w moim formacie:
    ndvi_bw.save("comp\\" + str(i) + "_bw_ndvi.jpg")  # saves picture in grayscale
    ndvi_col.convert("RGB").save("comp\\" + str(i) + "_col_ndvi.jpg")  # saves picture in color scale

    ndwi_bw.save("comp\\" + str(i) + "_bw_ndwi.jpg")  # saves picture in grayscale
    ndwi_col.convert("RGB").save("comp\\" + str(i) + "_col_ndwi.jpg")  # saves picture in color scale

    image.save("comp\\" + str(i) + "_org.jpg")  # saves original picture to compare

# funkcja działa wolno niestety, będziemy musieli zdecydować ktore zdjecie zostawimy albo nie wykonywac tego na stacji
# na miejszych zdjęciach 480/640 wykonuje się za to dosyć szybko
# można robić jedno zdjecie poglądowe w niskiej jakości, a jak będzie wysoka srednia ndvi to zdrobic drugie w lepszej
# i wtedy je analizować na ziemi

print('finish')
