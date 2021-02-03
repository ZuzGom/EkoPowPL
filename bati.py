import datetime
import requests
from bs4 import BeautifulSoup

# funnkcja która zwraca name, line1, line2 tak aktualne jak się tylko da
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
        back = open('celstrak.txt', 'a')
        back.write('\n' + str(czas) + '\n')
        back.write(name)
        back.write(line1)
        back.write(line2)
        back.close()

    else:  # jeśli nie ma połączenia wczytuje dane z pliku zapasowego
        f = open('celstrak.txt', 'r')
        linie = f.readlines()
        name = linie[-3]
        line1 = linie[-2]
        line2 = linie[-1]

    return czas, name, line1, line2


#print(track())
