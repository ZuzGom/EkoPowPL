# Converting image to NDVI colored scale

from PIL import ImageDraw, ImageFont  # Pillow library
import os

# p = "C:\\Projekty\\PicMatPlot\\"  # path to my test images folder


def index_convert(img):
    date, ext = os.path.splitext(img)
    # I get height and width of the image
    w, h = img.size

    # function below is useful, because it can be used to many various indexes defined after
    def operation(code, name, contrast):
        # ^^ kolejno: nazwa funkcji indeksu, nazwa do zapisania w pliku, funkcja kontrastu
        # for every single index, that's what happen:
        nonlocal img
        print('index: ' + name)
        index_col = img.copy().convert('HSV')  # creating hsv picture (h means color, i'll use it later)

        img_rgb = img.convert('RGB')
        index_bw = img_rgb.copy()  # creating copy for black-white index

        px_index_bw = index_bw.load()  # I get pixel information of b-w picture
        px_index_col = index_col.load()  # and hsv one
        index_sum = []  # list of every pixel's index

        # checking every single pixel

        for X in range(0, w):  # width
            for Y in range(0, h):  # height
                pixel_rgb = img_rgb.getpixel((X, Y))  # Get pixel's RGB values

                r, g, b = pixel_rgb

                # ~via Kuba Frączek
                brightness = sum(pixel_rgb) / 3  # 0 is dark (black) and 255 is bright (white)

                if 35 < brightness < 250:  # white and dark spots off
                    index = code(r, g, b)
                    index_sum.append(index)  # add index value to the list t.b.c.

                    index = contrast(index)  # a nice, suitable contrast

                    px_index_bw[X, Y] = (index, index, index)
                    # one picture in GRAYSCALE (r +b +g equals gray (or white (or black)))
                    px_index_col[X, Y] = (index, 200, 200)
                    # and one picture in HSV, in which H is index, so index value is one color of the spectrum
                    # i figured it out by myself ngl

        # print('zdjęcie nr. ' + str(i))  # Warum hier???

        # ####### skala ######

        s = int((h - 100) / 200)  # skala skali (sprawdzam ile razy w h miesci sie dlugosc skali)
        if s > 1:
            s -= 1  # zmiejszam i tak

        end = s * 200 + 100
        beg = 100

        # if average index value is too high or too low scale must adapt
        if sum(index_sum) / len(index_sum) > 0.4:
            end = h - 10
            if s > 1:
                s -= 1
        if sum(index_sum) / len(index_sum) < -0.4:
            beg = 10
            if s > 1:
                s -= 1
        # font = ImageFont.truetype("arial.ttf", 2 + s * 10)  # for windows
        font = ImageFont.truetype("FreeMono.ttf", 2 + s * 10)  # for linux

        for x in range(w - 10 - s * 10, w - 10):
            n = -0.2
            for y in range(beg, end):
                nv = contrast(n)  # the same contrast as at the picture
                px_index_bw[x, y] = (nv, nv, nv)
                px_index_col[x, y] = (nv, 200, 200)
                n += 0.003 / s

        ss = 32 * s  # odstępy między numerami
        hh = beg - 2  # początek skali

        # scale text on the hsv picture
        zo = ImageDraw.Draw(index_col)
        zo.text((w - 13 - s * 30, hh),          "-.2",  (0, 0, 200), font=font)
        zo.text((w - 13 - s * 30, hh + 1 * ss), "-.1",  (0, 0, 200), font=font)
        zo.text((w - 3 - s * 30, hh + 2 * ss),  "0",    (0, 0, 200), font=font)
        zo.text((w - 7 - s * 30, hh + 3 * ss),  ".1",   (0, 0, 200), font=font)
        zo.text((w - 7 - s * 30, hh + 4 * ss),  ".2",   (0, 0, 200), font=font)
        zo.text((w - 7 - s * 30, hh + 5 * ss),  ".3",   (0, 0, 200), font=font)
        zo.text((w - 7 - s * 30, hh + 6 * ss),  ".4",   (0, 0, 200), font=font)

        # scale on the grayscale picture
        za = ImageDraw.Draw(index_bw)
        za.text((w - 13 - s * 30, hh),          "-.2",  (255, 255, 255), font=font)
        za.text((w - 13 - s * 30, hh + 1 * ss), "-.1",  (255, 255, 255), font=font)
        za.text((w - 3 - s * 30, hh + 2 * ss),  "0",    (255, 255, 255), font=font)
        za.text((w - 7 - s * 30, hh + 3 * ss),  ".1",   (255, 255, 255), font=font)
        za.text((w - 7 - s * 30, hh + 4 * ss),  ".2",   (255, 255, 255), font=font)
        za.text((w - 7 - s * 30, hh + 5 * ss),  ".3",   (255, 255, 255), font=font)
        za.text((w - 7 - s * 30, hh + 6 * ss),  ".4",   (255, 255, 255), font=font)

        '''
        what scale does:
        - fits in any picture above 300 px height
        - change its value according to contrast on the picture
        - if the average index value is too high or too low, the scale can do mad things to fit
        - ...
        '''

        # nie moge zapisac w formacie hsv ;c (hsv my mistake)
        # zapisuje w moim formacie:

        # works on raspberry pi
        index_bw.save(date + "_bw_" + name + ".jpg")  # saves picture in grayscale
        index_col = index_col.convert("RGB")
        index_col.save(date + "_col_" + name + ".jpg")  # picture in color scale

        # works on my pc
        # index_bw.save(p + "final\\" + str(i) + "_bw_" + name + ".jpg")  # saves picture in grayscale
        # index_col.convert("RGB").save(p + "final\\" + str(i) + "_col_" + name + ".jpg")  # picture in color scale

        # print('worked')

        # kolejno: najmniejsza wartość, średnia i największa
        print(min(index_sum))
        print(sum(index_sum) / len(index_sum))
        print(max(index_sum))

    class Code:
        # I define indices functions (mostly) from:
        # https://www.int-arch-photogramm-remote-sens-spatial-inf-sci.net/XLII-3/1215/2018/isprs-archives-XLII-3-1215-2018.pdf
        # plus once I read:
        # because of the way the dyes are coupled to these layers, reproduce:
        # infrared as red, red as green, and green as blue.
        # do zrobienia: sprawdzić wszystkie indeksy w odsłonach normalnych i po powyższej zmianie

        @staticmethod
        def rgbvi(r, g, b):
            if (r - g) / (r + g) < -0.2:
                ix = -2
            else:
                ix = (g * g - r * b) / (g * g + r * b + 0.1)
            return ix

        @staticmethod
        def ndvi(r, g, b):
            ix = (r - b) / (r + b + 0.1)
            return ix

        @staticmethod
        def ndwi(r, g, b):
            ix = (r - g) / (r + g + 0.1)
            return ix

        @staticmethod
        def gli(r, g, b):
            if (r - g) / (r + g + 0.1) < -0.2:
                ix = -2
            else:
                ix = (2 * g - r - b) / (2 * g + r + b + 0.1)
            return ix

        @staticmethod
        def vari(r, g, b):
            if (r - g) / (r + g) < -0.2:
                ix = 2
            else:
                ix = (g - r) / (g + r - b + 0.1)
            return - ix

        @staticmethod
        def rgi(r, g, b):
            ix = r / (g + 0.1)
            return ix

        @staticmethod
        def ergbve(r, g, b):
            ix = 3.14159 * (g * g - r * b) / (g * g + r * b + 0.1)
            return ix

    # contrast function
    # every value below 0 ends up as 0, water starts at about -0.1, so I add 0.15
    # then I multiply it by 500 to make a good contrast
    # it cannot be float, because hsv and rgb can't read that ;c
    # different indexes need different contrast
    # after all I changed it randomly to make it look good

    def con(add, multi):
        def con_new(v):
            return int((v + add) * multi)
        return con_new

    # IMPORTANT! comment if needn't:

    '''
    operation(Code.vari, 'vari', con(0.15, 500))
    operation(Code.ergbve, 'ergbve', con(0.2, 300))
    operation(Code.gli, 'gli', con(0.01, 2000))
    operation(Code.rgbvi, 'rgbvi', con(0.2, 450))
    operation(Code.ndvi, 'ndvi', con(0.35, 300))
    operation(Code.rgi, 'rgi', con(-0.6, 200))
    '''

    operation(Code.ndwi, 'ndwi', con(0.2, 550))

    # w pythonie argumentami funkcji mogą być inne funkcje, czy to nie cudowne?


# #####################_MAIN_######################

# moje obrazy testowe są w formacie img1, img2... imgn więc...
# jesli chce przetestowac jeden z nich, to wpisuje jego liczbe i mam na wyjsciu ladnie zapisanie 1_ndvi, 1_hsv itd...
# zmodyfikowałam funkcję na tyle że w mainie wystarczy tylko otworzyć obraz
'''


for _ in range(14, 15):
    i = 3
    im = Image.open(p + "imgtest\\img15.jfif")
    image = Image.open(p + "imgtest\\img" + str(i) + ".jpg")

    # I get average and maximum NDVI value, ndvi pic and color pic
    index_convert(image)
    # I changed it, so index_convert is a separated function, which can be called on any picture

    image.save(p+"final\\" + str(i) + "_org.jpg")  # saves original picture to compare

# funkcja działa wolno niestety, będziemy musieli zdecydować ktore zdjecie zostawimy albo nie wykonywac tego na stacji
# na miejszych zdjęciach 480/640 wykonuje się za to dosyć szybko
# można robić jedno zdjecie poglądowe w niskiej jakości, a jak będzie wysoka srednia ndvi to zdrobic drugie w lepszej
# i wtedy je analizować na ziemi
'''
print('finish')
