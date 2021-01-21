import requests
from bs4 import BeautifulSoup

page = requests.get('http://www.celestrak.com/NORAD/elements/stations.txt')
soup = BeautifulSoup(page.content, 'html.parser')
page = soup.find()
