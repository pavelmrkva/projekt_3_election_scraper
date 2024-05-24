## Election scraper

Tento projekt stahuje a zpracovává volební data z webu [volby.cz](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) a ukládá je do CSV souboru.

## Instalace knihoven

V přiloženém souboru requirements.txt je seznam knihoven, které bude potřeba nainstalovat.
Pro instalaci (je doporučeno vytvořit nové virtuální prostředí) zadejte: 

`pip install -r requirements.txt`


## Spuštění projektu

v příkazovém řádku zadejte:

`python election_scraper.py 'URL okresu' 'název výstupního souboru.csv'`

## Ukázka projektu 
pro okres Kroměříž

`python election_scraper.py 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7201' 'vysledky_kromeriz.csv'`

průběh:

STAHUJI DATA Z VYBRANE URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=13&xnumnuts=7201

UKLADAM DO SOUBORU: vysledky_kromeriz.csv.
UKONCUJI election-scraper
 

Další url okresů získáte kliknutím na 'X' ve sloupci 'výběr obce' 

## Výstupní soubor
[vysledky_kromeriz.csv](vysledky_kromeriz.csv)