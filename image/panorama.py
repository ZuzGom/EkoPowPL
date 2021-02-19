from PIL import Image
import glob
import os
import matplotlib.pyplot as plt

"""
 This script merges photos into panorama and will be run on Earth
"""
cord = []  # used for saving coordinates from file
move = []  # used for moving coordinates
c = -1  # counter

w = 1920
h = 1080
names = []  # file names

# naming format:
# gg.mm.ss_lat_long.jpg
for infile in glob.glob("*.jpg"):  # reads every photo in script's localization, with .jpg extension

    file, ext = os.path.splitext(infile)
    names.append(file)  # file names without extensions

    img = Image.open(infile)
    w, h = img.size

    im = img.copy()
    im = im.convert('RGBA')

    px = im.load()
    for X in range(0, w):  # width
        for Y in range(0, h):  # height
            pixel_rgb = im.getpixel((X, Y))  # Get pixel's RGB values
            r, g, b, a = pixel_rgb
            brightness = (r + g + b) / 3
            if brightness < 50:  # if there's black, makes pixel transparent, unfortunately, clouds shadows are included
                px[X, Y] = (200, 200, 200, 0)
    im.save("new_" + file + ".png")  # new photo without frame

    file = file.split('_')
    file = file[1:]
    file[0] = file[0].split('.')
    cord.append(file)  # list with coordinates
    print(im)
    c += 1  # number of photos

print(cord)
for i in range(len(cord)):
    cord[i][0] = (int(cord[i][0][0]) * 3600 +
                  int(cord[i][0][1]) * 60 +
                  int(cord[i][0][2]))

for i in range(1, len(cord)):
    time1 = cord[-i][0] - cord[-i - 1][0]
    if time1 > 80000:
        time1 = 86400 - cord[-i][0] + cord[-i - 1][0]
    move.append([time1,
                 float(cord[-i][1]) - float(cord[-i - 1][1]),
                 float(cord[-i][2]) - float(cord[-i - 1][2])])
move = move[::-1]
print(move)
print(c)
x = []
y = []

if float(cord[0][1]) < 0:
    names = names[::-1]
for d in cord:
    x.append(float(d[1]))
    y.append(float(d[2]))
print(x, y)
plt.plot(x, y, 'ro')
# plt.axis([0, 10, 0, 10])
# plt.show()

p = 410  # x shift
q = 90  # y shift
# p = 350
# q = 45
size = (1920 + c * p + 500,
        1080 + c * q + 200)  # c * p, c * q, because we need as much shifts as number of photos
print(size)

result = Image.new('RGBA', size)  # final photo
wpx = result.load()  # final photo pixels
try:
    new = Image.open("new_" + names[0] + ".png")  # opens first file with .png extension
except IndexError:
    print('no photos!')
else:
    # inserts first photo to the final file
    for X in range(0, w):  # width
        for Y in range(0, h):  # height
            wpx[X, Y] = new.getpixel((X, Y))

    result.save("result0_new.png")


    def shift(a, b, new2):

        """
        Compares photo after shift with result
        """

        print(a, b)
        for X in range(0, w):  # width
            for Y in range(0, h):  # height
                try:
                    p = result.getpixel((X + a, Y + b))
                    # comparing begins in result place after a,b shift
                    p2 = new2.getpixel((X, Y))
                    r1, g1, b1, a1 = p
                    r2, g2, b2, a2 = p2
                    if a2 > 0:
                        if a1 > 0:
                            if p == p2:
                                wpx[X + a, Y + b] = p
                            else:
                                wpx[X + a, Y + b] = (int((r1 + r2) / 2),
                                                     int((g1 + g2) / 2),
                                                     int((b1 + b2) / 2), 300)
                        else:
                            wpx[X + a, Y + b] = p2

                except IndexError:
                    p2 = new2.getpixel((X, Y))
                    wpx[X + a, Y + b] = p2
        print("save" + str(i))
        result.save("panorama/result" + str(i) + "_new.png")


    # shifts are the same, so it can be done by for loop
    for i in range(1, c + 1):
        new1 = Image.open("new_" + names[i] + ".png")
        shift(i * p, i * q, new1)

    # deletes all .png files
    for x in names:
        os.remove("new_" + x + ".png")

    print(new)
    result.save("result_new.png")
    print(result)
