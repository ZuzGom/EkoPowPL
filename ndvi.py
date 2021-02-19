# Converting image to NDVI colored scale

from PIL import ImageDraw, ImageFont, Image  # Pillow library

data = open('index_convert.csv', 'w')
data.write("Name: ;Longtitude: ; Latitude: ;Index name: ;Maximum: ;Average: ;Minimum: \n")
data.close()


def index_convert(image, lon, lat):
    dr = ''
    path = image.split("/")
    for p in path[:-1]:
        dr += p + '/'
    dr += '/indicies/'
    date = '.'.join(path[-1].split('.')[:-1])
    img = Image.open(image)
    # I get height and width of the image
    w, h = img.size

    # function below is useful, because it can be used to many various indexes defined after
    def operation(code, name, contrast):
        # ^^ kolejno: nazwa funkcji indeksu, nazwa do zapisania w pliku, funkcja kontrastu
        # name of index func, name to save in file, contrast func

        # for every single index, that's what happen:
        nonlocal img, date
        global data
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

        # ####### scale ######

        s = int((h - 100) / 200)  # scale of the scale (I check how many times it could fit)

        if s > 2:
            s -= 2  # however its still to big, unless it would be too small to exist
        end = s * 200 + 100
        beg = 100

        # if average index value is too high or too low scale must adapt
        if sum(index_sum) / len(index_sum) > 0.4:
            end = h - 10
            if s > 1:
                s -= 1
        if sum(index_sum) / len(index_sum) < -0.4:
            beg = 10
            if s > 2:
                s -= 2
        try:
            font = ImageFont.truetype("DejaVuSansMono.ttf", 2 + s * 10)  # for linux
        except OSError:
            font = ImageFont.truetype("arial.ttf", 2 + s * 10)  # for windows

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
        - if the average index value is too high or too low, the scale can do things to fit
        - ...
        '''

        try:
            # works on raspberry pi:
            index_bw.save(dr + date + "_bw_" + name + ".jpg")  # saves picture in grayscale
            index_col = index_col.convert("RGB")
            index_col.save(dr + date + "_col_" + name + ".jpg")  # picture in color scale
        except (FileNotFoundError, OSError):
            index_bw.save(date + "_bw_" + name + ".jpg")  # saves picture in grayscale
            index_col = index_col.convert("RGB")
            index_col.save(date + "_col_" + name + ".jpg")  # picture in color scale

        # print('worked')

        # max value, average, and min
        data = open('index_convert.csv', 'a')
        data.write(str(date) + ';' +
                   str(lon) + ';' +
                   str(lat) + ';' +
                   str(name) + ';' +
                   str(min(index_sum)) + ';' +
                   str(sum(index_sum) / len(index_sum)) + ';' +
                   str(max(index_sum)) + ';' + '\n')

        data.close()

        dane = [name, (min(index_sum), sum(index_sum) / len(index_sum), max(index_sum))]
        return dane
    out = []

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
    
    '''
    out.append(operation(Code.ndwi, 'ndwi', con(0.2, 550)))
    out.append(operation(Code.ndvi, 'ndvi', con(0.35, 300)))
    out.append(operation(Code.rgi, 'rgi', con(-0.6, 200)))

    return out
