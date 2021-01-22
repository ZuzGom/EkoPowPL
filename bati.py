import requests
from bs4 import BeautifulSoup

page = requests.get('http://www.celestrak.com/NORAD/elements/stations.txt')
calosc = page.text
soup = BeautifulSoup(page.content, 'html.parser')
print(calosc)

