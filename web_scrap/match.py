'''
    In this file I get the game name for each one of 30 games like "Borussia Dortmund 0 - 2 Real Madrid". This title is extracted via each url appearing in 
    urls.txt that refers to live updates of each game.
'''

import requests
from bs4 import BeautifulSoup

urls = []
file_path = 'web_scrap/txt_files/urls.txt'


with open(file_path, 'r', encoding="utf-8") as file:
    for line in file:
        urls.append(line.strip())

matches = []

for ur_l in urls:

    url_1 = ur_l
    page = requests.get(url_1)
    soup = BeautifulSoup(page.content, 'html.parser')
    element = soup.find('h1', {'id': 'title_text_wide', 'itemprop': 'headline'})

    if element:
        text = element.get_text(strip=True).replace("Live Updates:", "")
        matches.append(text)
        print(text)
    else:
        print('Element not found')

with open("web_scrap/txt_files/matches.txt", "w", encoding="utf-8") as file:
    for match_ in matches:
        file.write(match_ + "\n")