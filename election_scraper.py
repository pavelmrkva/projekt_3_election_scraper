"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Pavel Mrkva
email: palon@seznam.cz
discord: pavel_58358
"""

import requests
from bs4 import BeautifulSoup
import sys
import csv

def get_town_codes(soup):
    town_codes = []
    for td in soup.find_all('td', class_='cislo'):
        for a in td.find_all('a'):
            town_codes.append(a.text)
    return town_codes

def get_town_names(soup):
    town_names = []
    for td in soup.find_all('td', class_='overflow_name'):
        town_names.append(td.text)
    return town_names

def get_town_links(soup):
    town_links = []
    for td in soup.find_all('td', class_='cislo'):
        for a in td.find_all('a'):
            town_links.append("https://volby.cz/pls/ps2017nss/" + a['href'])
    return town_links

def get_town_data(soup):
    voters = soup.find('td', headers='sa2').text.replace('\xa0', '')
    envelopes_issued = soup.find('td', headers='sa3').text.replace('\xa0', '')
    valid_votes = soup.find('td', headers='sa6').text.replace('\xa0', '')
    return voters, envelopes_issued, valid_votes

def get_party_names_and_votes(soup):
    party_names = []
    party_votes = []
    names = soup.find_all('td', class_='overflow_name')
    votes = soup.find_all('td', {'headers': ['t1sa2 t1sb3', 't2sa2 t2sb3']})

    for name in names:
        party_names.append(name.text.strip())
    
    for vote in votes:
        party_votes.append(vote.text.replace('\xa0', ''))
    
    return party_names, party_votes

def check_input_arguments():
    if len(sys.argv) != 3:
        print("Chybný počet argumentů.")
        print("Pro správné spuštění programu použijte následující formát:")
        print("python election_scraper.py <URL adresa> <název výstupního souboru.csv>")
        print("Příklad: python election_scraper.py 'https://volby.cz/pls/ps2017nss/...' 'vysledky.csv'")
        exit()
    if "https://volby.cz/pls/ps2017nss/" not in sys.argv[1]:
        print("Neplatná URL adresa.")
        print("Ujistěte se, že URL adresa začíná 'https://volby.cz/pls/ps2017nss/'")
        exit()
    if ".csv" not in sys.argv[2]:
        print("Neplatný název výstupního souboru.")
        print("Název výstupního souboru musí obsahovat příponu '.csv'.")
        exit()


def main():
    check_input_arguments()
    url = sys.argv[1]
    output_file = sys.argv[2]

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(f"STAHUJI DATA Z VYBRANE URL: {url}")

    town_codes = get_town_codes(soup)
    town_names = get_town_names(soup)
    town_links = get_town_links(soup)

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # Získat názvy stran a napsat hlavičku
        sample_response = requests.get(town_links[0])
        sample_soup = BeautifulSoup(sample_response.text, "html.parser")
        party_names, _ = get_party_names_and_votes(sample_soup)
        
        header = ["code", "location", "registered", "envelopes", "valid"]
        header.extend(party_names)
        writer.writerow(header)

        for i, link in enumerate(town_links):
            response = requests.get(link)
            town_soup = BeautifulSoup(response.text, "html.parser")
            voters, envelopes_issued, valid_votes = get_town_data(town_soup)
            party_names, party_votes = get_party_names_and_votes(town_soup)

            party_votes_dict = dict(zip(party_names, party_votes))

            row_data = [town_codes[i], town_names[i], voters, envelopes_issued, valid_votes]
            for party in party_names:
                row_data.append(party_votes_dict.get(party, '0'))  # Přidání hlasů pro danou stranu

            writer.writerow(row_data)

    print(f"UKLADAM DO SOUBORU: {output_file}.")
    print("UKONCUJI election-scraper")

if __name__ == "__main__":
    main()
