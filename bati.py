import requests
from bs4 import BeautifulSoup

def track():
    page = requests.get('http://www.celestrak.com/NORAD/elements/stations.txt')
    if (page.status_code == 200):
        calosc = str(page.text)
        soup = BeautifulSoup(page.content, 'html.parser')
        calosc = calosc.split('\n')
        name = calosc[0]
        line1 = calosc[1]
        line2 = calosc[2]

        return name, line1, line2
