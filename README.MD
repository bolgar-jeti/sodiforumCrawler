# Sodifórum Crawler 0.1.2
## Mi ez?
Ez egy olyan apró python tool, ami segítségével le lehet egy sqlite3 adatbázisba gyűjteni a sodifórumos kommenteket. Illetve most már elérhető hozzá egy flask script is, ami egy lokális webszervert indít, amelynek webes felületén könnyebben és kényelmesebben lehet keresni, mint az sql parancsokkal.

## Hogyan  működik?
A pipenv run getAllComments.py parancsot meghívva a kommenteket egy sfcomments nevezetű táblába szedi le a következő adatokkal (a Requests, BeautifulSoup és az SQLite3 python modulok segítségével):

- id -> A komment ID-ja.
- page -> Hányadik oldalon található a komment. 
- name -> A komment írójának neve
- verified -> A kommentelő regisztrált névvel írta-e a kommentet.
- comment -> Maga a komment.
- points -> A kommenten lévő pont.
- date -> A komment beküldésének időpontja.

A script 50 oldalanként vagy a legutolsó kommentig menti el teljesen az adatbázisba az adatokat. Megszakadás esetén a legutóbbi komment dátuma és visszaszámolva 3 napi kommentektől folytatja tovább. Így frissűlnek a legutóbbi előtt mentett kommentek pontszámai is.

Fontos(!): Most már képes a script updatelni a a kommentekhez tartozó pontszámokat!

Keresni a kommentek közt pedig úgy lehet, hogy a runServer.py van meghívva elindul egy webszerver és a localhost:3000 címen bejön a webes felület a kereső űrlappal. A webszerver akkor indítható, ha már eleve van adatbázis és vannak benne betöltött és mentett rekordok.

## "Én is szeretnék adatbázist! Hogyan tudom ezt használni?"
Először is le kell tölteni vagy clone-olni a script fájlokat innen githubról.
Fel kell telepíteni a lehető legfrissebb python-t. Majd python telepítése után a githubról leszedett forrásfájlok közt a dep_install.bat fájlt kell futtatni. Ilyenkor feltelepíti az összes szükséges modult a használathoz.

Ha minden sikeresen feltelepült, ezután szükség lesz a lokális adatbázisra, amit egyszerűen a következő fájl futtatásával lehet létrehozni és frissíteni:

getAllComments.bat

Ha teljesen nulláról indul, akkor eltarthat 1-2 óráig is a lokális adatbázis feltöltése kommentekkel. A script képes frissíteni az előző kommentek pontszámát és azt az adatot, hogy a komment melyik oldalon található meg. 50 oldalanként commitol (menti el a beolvasásokat) vagy amíg a kommentek végéhez nem ér a beolvasás.

Miután lefutott a script, azaz van egy olvasható adatbázis, el lehet indítani a webszervert. Ezt a következő fájl futattásával lehet:

runServer.bat

Ha minden szükséges modul sikeresen fel lett telepítve akkor gond nélkül futnia kell a webszervernek.

## "Nekem nem jó, eredetileg van már egy adatbázisom, de error-t dob"

Minden újabb frissítésnél érdemes új adatbázist kezdeni, hogy biztosan kompatibilis legyen a kezelése (pl. valami nem volt primary key, aminek az kellett volna lennie és ez okozhat gondot). Nem kell feltétlen törölni az előző adatbázis fájlt, egy kis "sql és python mágiával" pikk pakk átvihető az új adatbázisba az addigi kommentek. (Erről ha nem sodikázom el lehet csinálok egy scriptet később.)
