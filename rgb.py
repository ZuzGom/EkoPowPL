# Converting image to NDVI colored scale

from PIL import Image  # Pillow library
import os


def if_black(image):  # path to image
    img = Image.open(image)
    img = img.convert('RGB')
    w, h = img.size
    x = int(w/4)
    y = int(h/2)
    c = 0
    for X in range(x, 2*x):  # width
        for Y in range(y-5, y+5):  # height
            pixel_rgb = img.getpixel((X, Y))  # Get pixel's RGB values
            brightness = sum(pixel_rgb) / 3  # 0 is dark (black) and 255 is bright (white)
            if brightness > 30:
                c += 1
    if c > int(x):
        return False
    else:
        return True


def check_clouds(image):  # path to image
    counter=0
    date = '.'.join(os.path.basename(image).split('.')[:-1])  # image name
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


    for X in range(0, w):  # width
        for Y in range(0, h):  # height
            pixel_rgb = img_rgb.getpixel((X, Y))  # Get pixel's RGB values

            R, G, B = pixel_rgb

            r = (R-120)*2
            g = (G-120)*2
            b = (B-120)*2
            o = (b - g) * 5#0=0 CHMURY NIEMA o=255 JEST
            # to jednak nienajlepszy sposób (wariuje dla wody chociażby)
            # tak czy inaczej, Kamil jeśli to czytasz, możesz zrobić jakąkolwiek funkcję która sprawdza stężenie chmur
            # może być taka która liczy to co wyżej plus zwykłe białe piksele
            # i jak jest drastyczna różnica to powyższe ignoruje

            brightness = sum(pixel_rgb) / 3  # 0 is dark (black) and 255 is bright (white)

            if brightness > 130:

                px_b[X, Y] = (b, b, b)
                px_r[X, Y] = (r, r, r)
                px_g[X, Y] = (g, g, g)
                px_o[X, Y] = (b, b, b, o)
                counter +=1
                # transparentność "o" to miara ilości chmury, b b b sprawia, że wygląda to ładnie
                if o < 0:
                    px_o[X, Y] = (o, o, o, 0)
            else:
                px_b[X, Y] = (0, 0, 0)
                px_r[X, Y] = (0, 0, 0)
                px_g[X, Y] = (0, 0, 0)
                px_o[X, Y] = (0, 0, 0, 0)
    cp_clouds=counter/(w*h)*100
    blue.save("rgb\\" + date + "_blue.jpg")
    green.save("rgb\\" + date + "_green.jpg")
    red.save("rgb\\" + date + "_red.jpg")
    out.save("rgb\\" + date + "_zout.png")
    return cp_clouds
check_clouds("moon.jpg")
