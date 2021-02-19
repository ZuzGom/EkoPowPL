# coding: utf-8
# program written by EkoPowPL Team from Jaslo (Poland) for
# AstroPi competition 2020/2021
# Team Members: Zuzanna Gomuła, Jakub Frączek, Jakub Batycki, Kamil Kras, Bartosz Królikowski, Wojciech Lupa
# Teachers: Wincenty Skwarek
from time import sleep
from picamera import PiCamera
from datetime import datetime, timedelta
from threading import Thread
import sys
import os

from LightIntensity import lightIntensity
import sHat
from kordy import isstrack
from ndvi import index_convert
from rgb import if_black, check_clouds

sys.stdout = open('EkoPowPL.log', 'w')

start = datetime.now()

sHat.clear()
sHat.welcomeMessage()
path = sys.path

for x in path:
    print(x)

camera = PiCamera()
now = datetime.now()
amount_serie = 1
ln, lt = 0, 0


def getn():  # creates name with current data
    global now, ln, lt
    timest = now.strftime("%m.%d_%H.%M.%S_")
    ln, lt, cn = isstrack()
    timest += str(int(ln)) + '_' + str(int(lt)) + '_' + cn
    return timest


def high_def(img):
    camera.resolution = (2048, 1536)
    sHat.camera()
    camera.capture(img)


def low_def(img):
    camera.resolution = (480, 320)
    sHat.camera()
    camera.capture(img)

def analysis():
    global ln, lt
    dat = getn()
    name = 'image/' + dat + '.jpg'
    high_def(name)
    try:
        sHat.hourglass_s1()
        dane = index_convert(low, ln, lt)
        print(dane)
        sHat.hourglass_s2()
        lightIntensity(low, dat)
        sHat.hourglass_s3()

        if (dane[0][1][0]+dane[0][1][2]) < dane[0][1][1]:
            for _ in range(3):
                name = 'image/' + getn() + '.jpg'
                high_def(name)
                index_convert(name, ln, lt)
                sleep(10)

    except Exception as ex:
        print(type(ex), ex)


def taking_serie():
    global amount_serie
    for j in range(10):
        high_def("image/serie" + str(amount_serie) + "_" + str(j) + ".jpg")
        sleep(10)
    amount_serie += 1
    sHat.hourglass_s4()


last = datetime.now() - timedelta(minutes=10)
black = datetime.now()


while True:
    now = datetime.now()
    if now > start + timedelta(minutes=179):
        break
    if now > last + timedelta(minutes=5):
        last = datetime.now()
        date_time = now.strftime("%m.%d_%H.%M.%S_")
        lon, lat, country = isstrack()
        date = getn()
        print(date)
        low = 'image/low_' + date + '.jpg'
        low_def(low)
        if not if_black(low):
            if amount_serie < 9:
                Thread(target=analysis).start()
                if check_clouds(low, 'n') > 15:
                    Thread(target=taking_serie).start()
            else:
                analysis()
        else:
            black = datetime.now()
            os.remove(low)
            print('Night')
            sHat.nightTime()
    sleep(1)

# till the end less that 15 minutes left
low = 'image/low_' + getn() + '.jpg'
low_def(low)

sHat.clear()
sys.stdout.close()
