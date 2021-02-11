# Converting image to NDVI colored scale

from PIL import ImageDraw, ImageFont, Image  # Pillow library
import os


p = "C:\\Projekty\\PicMatPlot\\"  # path to my test images folder


def rgb_convert(image):
    dr = os.path.dirname(image)
    dr += '/indicies/'
    date = '.'.join(os.path.basename(image).split('.')[:-1])
    img = Image.open(image)
    # I get height and width of the image
    w, h = img.size

    img_rgb = img.convert('RGB')
    blue = img_rgb.copy()  # creating copy for black-white index
    red = img_rgb.copy()
    green = img_rgb.copy()
    img_rgb = img.convert('RGBA')
    out = img_rgb.copy()
    img_rgb = img.convert('RGB')

    px_b = blue.load()  # I get pixel information of b-w picture
    px_r = red.load()  # and hsv one
    px_g = green.load()
    px_o = out.load()
    index_sum = []  # list of every pixel's index

    # checking every single pixel

    for X in range(0, w):  # width
        for Y in range(0, h):  # height
            pixel_rgb = img_rgb.getpixel((X, Y))  # Get pixel's RGB values

            R, G, B = pixel_rgb
            r = (R-120)*2
            g = (G-120)*2
            b = (B-120)*2
            o = (b - g) * 5
            if o < 0:
                o = 0

            # ~via Kuba Frączek
            brightness = sum(pixel_rgb) / 3  # 0 is dark (black) and 255 is bright (white)

            if brightness > 130:  # white and dark spots off

                px_b[X, Y] = (b, b, b)
                px_r[X, Y] = (r, r, r)
                px_g[X, Y] = (g, g, g)
                px_o[X, Y] = (b, b, b, o)
                if o < 0:
                    px_o[X, Y] = (o, o, o, 0)
            else:
                px_b[X, Y] = (0, 0, 0)
                px_r[X, Y] = (0, 0, 0)
                px_g[X, Y] = (0, 0, 0)
                px_o[X, Y] = (0, 0, 0, 0)
                # one picture in GRAYSCALE (r +b +g equals gray (or white (or black)))
                # and one picture in HSV, in which H is index, so index value is one color of the spectrum
                # i figured it out by myself ngl
    print(px_o[100,100])
    blue.save(p + "rgb\\" + date + "_blue.jpg")
    green.save(p + "rgb\\" + date + "_green.jpg")
    red.save(p + "rgb\\" + date + "_red.jpg")
    out.save(p + "rgb\\" + date + "_zout.png")
    img_rgb.save(p + "rgb\\" + str(i) + "_org.jpg")


        # print('zdjęcie nr. ' + str(i))  # Warum hier???

        # ####### skala ######



# #####################_MAIN_######################

# moje obrazy testowe są w formacie img1, img2... imgn więc...
# jesli chce przetestowac jeden z nich, to wpisuje jego liczbe i mam na wyjsciu ladnie zapisanie 1_ndvi, 1_hsv itd...
# zmodyfikowałam funkcję na tyle że w mainie wystarczy tylko otworzyć obraz

num = [2, 4, 15]

for i in num:
    #im = Image.open(p + "imgtest\\img15.jfif")
    image = (p + "imgtest\\img" + str(i) + ".jpg")

    # I get average and maximum NDVI value, ndvi pic and color pic
    rgb_convert(image)
    # I changed it, so index_convert is a separated function, which can be called on any picture

      # saves original picture to compare

# funkcja działa wolno niestety, będziemy musieli zdecydować ktore zdjecie zostawimy albo nie wykonywac tego na stacji
# na miejszych zdjęciach 480/640 wykonuje się za to dosyć szybko
# można robić jedno zdjecie poglądowe w niskiej jakości, a jak będzie wysoka srednia ndvi to zdrobic drugie w lepszej
# i wtedy je analizować na ziemi
'''
index_convert('image\\image.jpg')
index_convert('image\\image (1).jpg')
'''
print('finish')
