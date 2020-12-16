drogi = [[1, 2, 3], [3, 2, 1], [ 4,3, 2]]


while 1 in drogi[0]:
    drogi[0].remove(1)
print(drogi)


A=[]
tab=[[]]

#tworzenie tablicy (pokraczne)

A = [None] * n
for i in range(n):
   A[i] = [None] * 3

for x in range(n):
   for y in range(3):
       A[x][y]=(int(input()))

#wczytywaine tablicy po liniach

for _ in range (n):
    first=input().split()
    tab.append(first)

#gługość słów w napisie
napis = 'Odwazny rudy lis przeskoczyl nad spiacym wilczurem'
slowa = napis.split()
dlugosc_slow = [len(slowo) for slowo in slowa]

#bez wcześniejszego deklarowania ilości elementów
B=[]
for x in range(4):
    B.append([])
    for y in range(3):
        B[x].append(y)

#dodawanie elementy tabeli
tab.apppend(x)
#dwuwymiarowej
tab[0].appepend(x)
del A[0] #lub usuwanie
tab.insert(1,'a')  # Dodawanie elementu w miejsce o indeksie 1

moja_lista=[1,2,3,4,5]
nowa_lista=[]
#wycinanie
moja_lista[:3] # elementy od pierwszego (domyślnie jeśli nie podano) do trzeciego: [1,2,3]
moja_lista[2:] # od trzeciego do ostatniego [3,4,5]
moja_lista[:] # wszystkie elementy listy [1,2,3,4,5]
moja_lista[-2:] # dwa ostatnie elementy [4,5]
moja_lista[:-1] # od pierwszego do przedostatniego [1,2,3,4]
moja_lista[3:-3] # od czwartego do czwartego od końca [3]
moja_lista[::2] # Wyświetl wszystko, ale co drugi element listy [1,3,5]
moja_list[::-1] # odwrócenie kolejności listy – wyświetlenie elementów od końca do początku [5, 4, 3, 2, 1]

nowa_lista.remove('a')  # Usunięcie z listy pierwszego wystąpienia zmiennej 'a'
nowa_lista.pop(0)       # Usunięcie z listy elementu o indeksie 0
nowa_lista.pop()        # Usunięcie ostatniego elementu listy
nowa_lista.index('a',1,10)       # Zwraca indeks pierwszego wystąpienia szukanego elementu w liście w zakresie
set(nowa_lista)         #usuwanie duplikatów
sum(lista)              #sumowanie listy

'a' in nowa_lista        # Prawda (True) jeśli element występuje w liście, w przeciwnym przypadku fałsz (False)
nowa_lista.count('a')   # Zwraca liczbę wystąpień elementu listy
max(nowa_lista)         # Zwraca największy element listy
min(nowa_lista)         # Najmniejszy element listy



#metody printu
print(lista_A [0:3])
print(A)
print(A+tab)
for x in A:
    print (x)

# A function that returns the length of the value:
def myFunc(e):
  return len(e)

#tyle sposobów na kopiowanie listy, a żaden nich nie działa

pomoc=list(drogi)

pomoc = drogi[:]

li_copy = []
li_copy.extend(li1)

li_copy = [i for i in li1]

#sortowanie
cars = ['Ford', 'Mitsubishi', 'BMW', 'VW']
cars.sort(reverse=True, key=myFunc)

cars[1:] = sorted(cars[1:])


#sortowanie w zakresie
drogi = [[1, 2, 3], [3, 2, 1], [4, 3, 2]]


for x in range(3):
    drogi[x][:2]=sorted(drogi[x][:2])
print(drogi)

#dodawanie elementów listy int
drogi[0][1] += drogi[0][2]

#dodawanie całej listy str
suma = int(''.join([str(elem) for elem in A])) + int(''.join([str(elem) for elem in tab]))