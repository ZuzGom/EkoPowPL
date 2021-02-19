from PIL import Image
import glob
import os
import matplotlib.pyplot as plt
"""
 This script will be used for merging photos into panorama, 
 and will be run on Earth
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

    # raz powstałe nie muszą się nadpisywać
    px = im.load()  # piksele im
    for X in range(0, w):  # width
        for Y in range(0, h):  # height
            pixel_rgb = im.getpixel((X, Y))  # Get pixel's RGB values
            r, g, b, a = pixel_rgb
            brightness = (r + g + b) / 3
            if brightness < 50:  # jesli jest czarno, przeroczystość na maksa, niestety cienie chmur odpadają
                px[X, Y] = (200, 200, 200, 0)
    im.save("new_" + file + ".png")  # nowe zdjęcie bez ramki


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
    czas = cord[-i][0] - cord[-i - 1][0]
    if czas > 80000:
        czas = 86400 - cord[-i][0] + cord[-i - 1][0]
    move.append([czas,
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

p = 410  # przesunięcie x
q = 90  # przesunięcie y
# p = 350
# q = 45
size = (1920 + c * p + 500,
        1080 + c * q + 200)  # c * p, bo tyle przesunięć ile zdjęć z założeniem że przesunięcie jest takie samo
print(size)

wynik = Image.new('RGBA', size)  # zdjęcie końcowe
wpx = wynik.load()  # piksele tegoż
try:
    new = Image.open("new_" + names[0] + ".png")  # otwieram pierwszy png
except IndexError:
    print('brak zdjęć!')
else:
    # do wynikowego zdjęcia wpisuję pierwsze z nich
    for X in range(0, w):  # width
        for Y in range(0, h):  # height
            wpx[X, Y] = new.getpixel((X, Y))

    wynik.save("wynik0_new.png")


    def przesuniecie(a, b, new2):
        print(a, b)
        # funckja porównuje zdjęcie po przesunięciu z wynikiem
        for X in range(0, w):  # width
            for Y in range(0, h):  # height
                try:
                    p = wynik.getpixel((X + a, Y + b))  # wygląda to tak:
                    # porównywanie nowego zdjęcia zaczyna się w miejscu wyniku po przsunięciu a,b
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

                except IndexError:  # błąd zawsze może się zdażyć
                    p2 = new2.getpixel((X, Y))
                    wpx[X + a, Y + b] = p2
        print("save" + str(i))
        wynik.save("panorama/wynik" + str(i) + "_new.png")


    '''
    #peóby zabawy z czasem
    past1 = 0
    past2 = 1

    for i in range(1, c+1):
        new1 = Image.open("new_" + names[i] + ".png")
        przesuniecie(past1 + int(move[i-1][0] * 31.7), past2 + int(move[i-1][0] * 7), new1)
        past1 += int(move[i-1][0] * 31.5)
        past2 += int(move[i-1][0] * 6.5)

    przesuniecie(350, 45, new2)
    przesuniecie(2*350, 2*45, new3)
    '''
    # przesunięcia takie same więc daje for
    for i in range(1, c + 1):
        new1 = Image.open("new_" + names[i] + ".png")      
        przesuniecie(i * p, i * q, new1)


# można w tym miejscu usunąć wszystkie png
    for x in names:
        os.remove("new_" + x + ".png")
    print(new)
    wynik.save("wynik_new.png")
    print(wynik)

