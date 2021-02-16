from sense_hat import SenseHat

sense = SenseHat()
sense.clear()

gr = (130, 130, 130)  # gray
aW = (200, 200, 200)  # almost White
dG = (0, 70, 0)  # dark green
lG = (0, 255, 0)  # light green
rG = (0, 140, 0)  # regular green
aB = (50, 50, 50)  # almost black
em = (0, 0, 0)  # empty
re = (255, 0, 0)  # red
yl = (255, 255, 0)  # yellow
pu = (60, 30, 60)  # purple
tl = (50, 50, 50)  # metalic
sa = (139, 90, 20)  # sand

Msense_camera = [

    em, em, em, em, em, em, em, em,
    em, em, rG, rG, rG, rG, em, em,
    gr, aW, aW, rG, rG, rG, rG, lG,
    dG, dG, rG, aB, aB, rG, lG, lG,
    dG, rG, aB, gr, aW, aB, rG, lG,
    dG, rG, aB, aW, aW, aB, rG, lG,
    dG, rG, rG, aB, aB, rG, rG, lG,
    em, em, em, em, em, em, em, em,

]

Mnight_time = [

    pu, pu, pu, pu, pu, pu, pu, pu,
    pu, pu, pu, yl, yl, yl, pu, pu,
    pu, pu, yl, yl, yl, pu, pu, pu,
    pu, pu, yl, yl, pu, pu, pu, pu,
    pu, pu, yl, yl, pu, pu, pu, pu,
    pu, pu, yl, yl, yl, pu, pu, pu,
    pu, pu, pu, yl, yl, yl, pu, pu,
    pu, pu, pu, pu, pu, pu, pu, pu,
]

Mhourglass_s1 = [

    em, tl, tl, tl, tl, tl, tl, em,
    em, tl, sa, sa, sa, sa, tl, em,
    em, em, tl, sa, sa, tl, em, em,
    em, em, em, tl, tl, em, em, em,
    em, em, em, tl, tl, em, em, em,
    em, em, tl, em, em, tl, em, em,
    em, tl, em, em, em, em, tl, em,
    em, tl, tl, tl, tl, tl, tl, em,
]

Mhourglass_s2 = [

    em, tl, tl, tl, tl, tl, tl, em,
    em, tl, em, em, em, sa, tl, em,
    em, em, tl, sa, sa, tl, em, em,
    em, em, em, tl, tl, em, em, em,
    em, em, em, tl, tl, em, em, em,
    em, em, tl, sa, em, tl, em, em,
    em, tl, sa, sa, em, em, tl, em,
    em, tl, tl, tl, tl, tl, tl, em,
]

Mhourglass_s3 = [

    em, tl, tl, tl, tl, tl, tl, em,
    em, tl, em, em, em, em, tl, em,
    em, em, tl, em, sa, tl, em, em,
    em, em, em, tl, tl, em, em, em,
    em, em, em, tl, tl, em, em, em,
    em, em, tl, sa, em, tl, em, em,
    em, tl, sa, sa, sa, sa, tl, em,
    em, tl, tl, tl, tl, tl, tl, em,
]

Mhourglass_s4 = [

    em, tl, tl, tl, tl, tl, tl, em,
    em, tl, em, em, em, em, tl, em,
    em, em, tl, em, em, tl, em, em,
    em, em, em, tl, tl, em, em, em,
    em, em, em, tl, tl, em, em, em,
    em, em, tl, sa, sa, tl, em, em,
    em, tl, sa, sa, sa, sa, tl, em,
    em, tl, tl, tl, tl, tl, tl, em,
]

def welcomeMessage():
    sense.show_message("Hello ISS! Greetings from EkoPowPL!", scroll_speed=(0.08))


def camera():
    sense.clear()
    sense.set_pixels(Msense_camera)


def nightTime():
    sense.clear()
    sense.set_pixels(Mnight_time)


def hourglass_s1():
    sense.clear()
    sense.set_pixels(Mhourglass_s1)


def hourglass_s2():
    sense.clear()
    sense.set_pixels(Mhourglass_s2)


def hourglass_s3():
    sense.clear()
    sense.set_pixels(Mhourglass_s3)


def hourglass_s4():
    sense.clear()
    sense.set_pixels(Mhourglass_s4)


def clear():
    sense.clear()
