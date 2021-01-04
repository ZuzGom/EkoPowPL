# Converting image to NDVI colored scale

# UWAGA! używam słów hsl i hsv wymiennie nie pomylcie się :3

from PIL import Image, ImageDraw, ImageFont  # Pillow library
import matplotlib.pyplot as plt

def NDVIconvert(img):
    # I get height and widith of the image
    w, h = img.size
    
    # function below is usefull, because it can be used to many various indexes defined after
    def operation(code, name, img, con):  
        # ^^ kolejno: nazwa funkcji indeksu, nazwa do zapisania w pliku, obraz na któym jest wywołana funkcja, funkcja kontrastu
        # for every single index, thats what hapenn:
        
        print('index: '+name)
        index_col = img.copy().convert('HSV')  # creating hsv picture (h means color, i'll use it later)

        img_rgb = img.convert('RGB')
        index_bw = img_rgb.copy()  # creating copy for black-white index

        px_index_bw = index_bw.load()  # I get pixel information of b-w picture
        px_index_col = index_col.load()  # and hsl one
        indexSum = []  # list of every pixel's index
        
        # checking every single pixel
        
        for X in range(0, w):  # widith
            for Y in range(0, h):  # height
                pixelRGB = img_rgb.getpixel((X, Y))  # Get pixel's RGB values

                r, g, b = pixelRGB

                # ~via Kuba Frączek
                Brightness = sum(pixelRGB) / 3  # 0 is dark (black) and 255 is bright (white)

                if 35 < Brightness < 180: # white and dark spots off
                    index = code(r, g, b)
                    indexSum.append(index)  # add index value to the list t.b.c.

                    index = con(index)  # a nice, suitable contrast

                    px_index_bw[X, Y] = (index, index, index)  # one picture in GRAYSCALE (r +b +g equals gray (or wihte (or black)))
                    px_index_col[X, Y] = (index, 200, 200)
                    # and one picture in HSL, in which H is index, so index value is one color of the scpectrum
                    # i figured it out by myself ngl

        print('zdjęcie nr. ' + str(i))  # Warum hier???

        # ####### skala ######

        s = int((h - 100) / 200)  # skala skali (sprawdzam ile razy w h miesci sie dlugosc skali)
        if s > 1:
            s -= 1  # zmiejszam i tak

        font = ImageFont.truetype("arial.ttf", 2 + s * 10)

        for x in range(w - 10 - s * 10, w - 10):
            n = -0.2
            for y in range(100, s * 200 + 100):
                nv = con(n)  # the same contrast as at picture
                px_index_bw[x, y] = (nv, nv, nv)
                px_index_col[x, y] = (nv, 200, 200)
                n += 0.003 / s

            ss = 32 * s  # odstępy między numerami
            hh = 100 - 2  # początek skali

            # scale text on the hsv picture
            zo = ImageDraw.Draw(index_col)
            zo.text((w - 13 - s * 30, hh), "-.2", (0, 0, 200), font=font)
            zo.text((w - 13 - s * 30, hh + 1 * ss), "-.1", (0, 0, 200), font=font)
            zo.text((w - 3 - s * 30, hh + 2 * ss), "0", (0, 0, 200), font=font)
            zo.text((w - 7 - s * 30, hh + 3 * ss), ".1", (0, 0, 200), font=font)
            zo.text((w - 7 - s * 30, hh + 4 * ss), ".2", (0, 0, 200), font=font)
            zo.text((w - 7 - s * 30, hh + 5 * ss), ".3", (0, 0, 200), font=font)
            zo.text((w - 7 - s * 30, hh + 6 * ss), ".4", (0, 0, 200), font=font)

            # scale on the grayscale picture
            za = ImageDraw.Draw(index_bw)
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

        # nie moge zapisac w formacie hsl ;c (hsv my mistake)
        # zapisuje w moim formacie:
        index_bw.save("comp\\" + str(i) + "_bw_"+name+".jpg")  # saves picture in grayscale
        index_col.convert("RGB").save("comp\\" + str(i) + "_col_"+name+".jpg")  # saves picture in color scale
        
        # kolejno: najmniejsza wartość, średnia i największa
        print(min(indexSum))
        print(sum(indexSum) / len(indexSum))
        print(max(indexSum))

        
    # I define indexes function
    # from: https://www.int-arch-photogramm-remote-sens-spatial-inf-sci.net/XLII-3/1215/2018/isprs-archives-XLII-3-1215-2018.pdf
    # plus once I read: because of the way the dyes are coupled to these layers, reproduce infrared as red, red as green, and green as blue.
    
    def rgbvi(r,g,b):
        ix = (g*g - r*b) / (g*g + r*b)
        return -ix

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

    def gli(r,g,b):
        ix = (2*g -r -b) / (2*g + r + b)
        return ix
    
    def vari(r,g,b):
        if (g+r-b) != 0:
            ix = (g-r)/(g+r-b)
        else:
            ix = 0
        return - ix

    # contrast function
    # every value below 0 ends up as 0, water starts at about -0.1, so I add 0.15
    # then I multiply it by 500 to make a good contrast
    # it cannot be float, because hsv and rgb can't read that ;c
    # different indexes need different contrast
    # after all i changed it randomly to make it look good

    def c1(v):
        return int((v + 0.2) * 400)
    def c2(v):
        return int((v + 0.2) * 550)
    def c3(v):
        return int((v + 0.01) * 2000)
    def c4(v):
        return int((v - 0.1) * 500)

    operation(rgbvi, 'rgbvi', img, c1)
    operation(ndvi, 'ndvi', img, c1)
    operation(ndwi, 'ndwi', img, c2)
    operation(gli, 'gli', img, c3)
    operation(vari, 'vari', img, c2)
    # w pythonie argumentami funkcji mogą być inne funkcje, czy to nie cudowne?


# #####################_MAIN_######################

# moje obrazy testowe są w formacie img1, img2... imgn więc...
# jesli chce przetestowac jeden z nich, to wpisuje jego liczbe i mam na wyjsciu ladnie zapisanie 1_ndvi, 1_hsl itd...
# zmodyfikowałam funkcję na tyle że w mainie wystarczy tylko otworzyć obraz

for x in range(14, 15):
    i = ''

    image = Image.open("imgtest\\img" + str(i) + ".jpg")

    # I get average and maximum NDVI value, ndvi pic and color pic
    NDVIconvert(image)
    # I changed it, so NDVIconvert is separated function, which can be called on any picture

    image.save("comp\\" + str(i) + "_org.jpg")  # saves original picture to compare

# funkcja działa wolno niestety, będziemy musieli zdecydować ktore zdjecie zostawimy albo nie wykonywac tego na stacji
# na miejszych zdjęciach 480/640 wykonuje się za to dosyć szybko
# można robić jedno zdjecie poglądowe w niskiej jakości, a jak będzie wysoka srednia ndvi to zdrobic drugie w lepszej
# i wtedy je analizować na ziemi

print('finish')
