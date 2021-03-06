# RGB based functions

from PIL import Image  # Pillow library


def if_black(image):  # path to image
    img = Image.open(image)
    img = img.convert('RGB')
    w, h = img.size
    x = int(w / 4)
    y = int(h / 2)
    c = 0
    for X in range(x, 2 * x):  # width
        for Y in range(y - 5, y + 5):  # height
            pixel_rgb = img.getpixel((X, Y))  # Get pixel's RGB values
            brightness = sum(pixel_rgb) / 3  # 0 is dark (black) and 255 is bright (white)
            if brightness > 30:
                c += 1
    if c > int(x):
        return False
    else:
        return True


def check_clouds(image, c):  # path to image
    counter = 0
    path = image.split("/")[-1]
    date = '.'.join(path.split('.')[:-1])  # image name
    img = Image.open(image)
    # I get height and width of the image
    w, h = img.size

    img_rgb = img.convert('RGB')
    blue = img_rgb.copy()
    red = img_rgb.copy()
    green = img_rgb.copy()
    img_rgb = img.convert('RGBA')
    out = img_rgb.copy()
    img_rgb = img.convert('RGB')

    px_b = blue.load()
    px_r = red.load()
    px_g = green.load()
    px_o = out.load()

    for X in range(0, w):  # width
        for Y in range(0, h):  # height

            pixel_rgb = img_rgb.getpixel((X, Y))  # Get pixel's RGB values

            R, G, B = pixel_rgb

            r = (R - 120) * 2
            g = (G - 120) * 2
            b = (B - 120) * 2
            o = (b - g) * 5

            brightness = sum(pixel_rgb) / 3  # 0 is dark (black) and 255 is bright (white)
            if c == 'y':
                if brightness > 130:

                    px_b[X, Y] = (b, b, b)
                    px_r[X, Y] = (r, r, r)
                    px_g[X, Y] = (g, g, g)
                    px_o[X, Y] = (b, b, b, o)
                    counter += 1
                    # o's transparency is measure of cloud amount, b b b makes it look better
                    if o < 0:
                        px_o[X, Y] = (o, o, o, 0)
                else:
                    px_b[X, Y] = (0, 0, 0)
                    px_r[X, Y] = (0, 0, 0)
                    px_g[X, Y] = (0, 0, 0)
                    px_o[X, Y] = (0, 0, 0, 0)
                try:
                    blue.save("rgb/" + date + "_blue.jpg")
                    green.save("rgb/" + date + "_green.jpg")
                    red.save("rgb/" + date + "_red.jpg")
                    out.save("rgb/" + date + "_zout.png")
                except FileNotFoundError:
                    blue.save(date + "_blue.jpg")
                    green.save(date + "_green.jpg")
                    red.save(date + "_red.jpg")
                    out.save(date + "_zout.png")
            else:
                if brightness > 130:
                    counter += 1
    cp_clouds = counter / (w * h) * 100

    print('Clouds concentration: ' + str(cp_clouds))
    return cp_clouds
