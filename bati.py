import datetime
import requests
from bs4 import BeautifulSoup


def track():
    czas = datetime.datetime.now()
    godzina = czas.hour
    page = requests.get('http://www.celestrak.com/NORAD/elements/stations.txt')
    if page.status_code == 200:

        calosc = str(page.text)
        soup = BeautifulSoup(page.content, 'html.parser')
        calosc = calosc.split('\n')
        name = calosc[0]
        line1 = calosc[1]
        line2 = calosc[2]

        back = open('kordynaty.txt', 'a')
        back.write(name)
        back.write(line1)
        back.write(line2)
        back.close()
    else:
        f = open('kordynaty.txt', 'r')
        linie = f.readlines
        name, line1, line2, = linie[:-3]

        # return name, line1, line2
    return godzina, name, line1, line2
print(track())