import requests
from bs4 import BeautifulSoup

page = requests.get('http://www.celestrak.com/NORAD/elements/stations.txt')
if(page.status_code==200):
    calosc = str(page.text)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(calosc)

