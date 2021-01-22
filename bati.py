import requests
from bs4 import BeautifulSoup

page = requests.get('http://www.celestrak.com/NORAD/elements/stations.txt')
if(page.status_code==200):
    calosc = page.text
    soup = BeautifulSoup(page.content, 'html.parser')
    #calosc.split('\n').[:3]

    MyFile = open("kordynaty.txt", "w")
    MyFile.write(calosc)
    MyFile.close()

    MyFile = open("kordynaty.txt", "r")
    for i in range(6):
        print(MyFile.readline())
    MyFile.close()
else:
    print("Strona nie dziala")

