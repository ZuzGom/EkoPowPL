from PIL import Image
import glob
import os


cord = []  # to służy do zapisu koordynatów z nazwy pliku
move = []  # a to do ich przesunięcia
c = -1  # counter

# im.size niedziała - do naprawienia
w = 1920
h = 1080
names = []  # nazwy plików

# mam to stąd:
# https://pillow.readthedocs.io/en/stable/reference/Image.html

# zdjęcia niech będą w formacie:
# gg:mm:ss_lat_long.jpg
for infile in glob.glob("*.jpg"):  # czyta każde zdjęcie w lokalizacji o rozszerzeniu.jpg

    file, ext = os.path.splitext(infile)
    names.append(file)  # nazwy plików bez rozszerzenia, przydadzą się poźniej

    img = Image.open(infile)

    im = img.copy()  # po co kopia? nie wiem
    im = im.convert('RGBA')
    px = im.load()  # piksele im

    for X in range(0, w):  # width
        for Y in range(0, h):  # height
            pixel_rgb = im.getpixel((X, Y))  # Get pixel's RGB values
            r, g, b, a = pixel_rgb
            brightness = (r + g + b)/3
            if brightness < 50:  # jesli jest czarno, przeroczystość na maksa, niestety cienie chmur odpadają
                px[X, Y] = (200, 200, 200, 0)
    cord.append(file.split('_'))  # lista z kordami
    im.save("new_"+file + ".png")  # nowe zdjęcie bez ramki
    print(im)  # czytam czy się wszystko udało
    c += 1  # liczy ile zdjęć będzie łączonych (jaki musi być rozmiar wyniku)

# skomentowałam to bo wywalał błąd
'''
print(cord)
for i in range(1, len(cord)):
    try:
        move.append([float(cord[-i][1])-float(cord[-i-1][1]),
                 float(cord[-i][2])-float(cord[-i-1][2])])
    
print(move)
print(c)
'''

p = 410  # przesunięcie x
q = 90  # przesunięcie y

size = (1920 + c*p, 1080+c*q)  # c * p, bo tyle przesunięć ile zdjęć z założeniem że przesunięcie jest takie samo
print(size)


wynik = Image.new('RGBA', size)  # zdjęcie końcowe
wpx = wynik.load()  # piksele tegoż


new = Image.open("new_"+names[0]+".png")  # otwieram pierwszy png

# do wynikowego zdjęcia wpisuję pierwsze z nich
for X in range(0, w):  # width
    for Y in range(0, h):  # height
        wpx[X, Y] = new.getpixel((X, Y))


def przesuniecie(a, b, new2):
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
                                                 int((b1 + b2) / 2), 255)
                    else:
                        wpx[X + a, Y + b] = p2

            except IndexError:  # błąd zawsze może się zdażyć
                p2 = new2.getpixel((X, Y))
                wpx[X + a, Y + b] = p2


'''
przesuniecie(350, 45, new2)
przesuniecie(2*350, 2*45, new3)
'''
# przesunięcia takie same więc daje for
for i in range(1, c):
    new1 = Image.open("new_"+names[i]+".png")
    przesuniecie(i*p, i*q, new1)

# można w tym miejscu usunąć wszystkie png
for infile in glob.glob("*.png"):
    os.remove(infile)
print(new)
wynik.save("wynik_new.png")
