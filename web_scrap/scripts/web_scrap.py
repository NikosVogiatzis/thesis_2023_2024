# This script is responsible for extracting the url's from 30 latest match results for champions league
# it is implemented with BeautifulSoup 
# after retrieving the urls, they get saved in a file urls.txt in directory web_scrap/txt_files/
# i also extract the match name (basically the result form Live Updates title) and store each match result 
# in a file matches.txt (e.g: Borussia Dortmund 0 - 2 Real Madrid). I do that so that when i implement the ner and relationships extractions. 
# each even should get associated with the match that it took place

import requests
from bs4 import BeautifulSoup


url = 'https://www-sportsmole-co-uk.translate.goog/football/champions-league/results.html?_x_tr_sl=en&_x_tr_tl=el&_x_tr_hl=el&_x_tr_pto=sc'

page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

# Find all elements with class name specified and store them inside doc list
url_elements = soup.find_all(class_='l_sfp_links')

urls = []

# for each element inside url_elements, grab the href to match details url
for element in url_elements:
   if 'href' in element.attrs:
        href = element['href']
        urls.append(href)

# Shorten the list to 30 urls
urls = urls[:30]
i = 0


# Find all tags that contain the href link to the page containing the live commentary

tags_to_commentary = []

for ur_l in urls:

    url_1 = ur_l
    page1 = requests.get(url_1)

    soup1 = BeautifulSoup(page1.content, 'html.parser')

    # find all elements containing an href that has ('live updates' in the url -> concluded via page inspect)
    
    target_tag = soup1.find('a', href=lambda href: href and 'live-updates' in href)
    tags_to_commentary.append(target_tag)
       
# for each tag found previously grab the url to the live commentary (30 live commentary urls)

links_to_commentary = []
for element in tags_to_commentary:
    if 'href' in element.attrs:
        href = element['href']
        links_to_commentary.append(href)

# Write all urls in the file urls.txt

file_path = "web_scrap/txt_files/urls.txt"


with open(file_path, 'w') as file:
    for item in links_to_commentary:
        file.write(item + '\n')



matches = []

for ur_l in links_to_commentary:

    url_1 = ur_l
    page = requests.get(url_1)
    soup1 = BeautifulSoup(page.content, 'html.parser')
    element = soup1.find('h1', {'id': 'title_text_wide', 'itemprop': 'headline'})

    if element:
        text = element.get_text(strip=True).replace("Live Updates:", "")
        matches.append(text)
        print(text)
    else:
        print('Element not found')

with open("web_scrap/txt_files/matches.txt", "w", encoding="utf-8") as file:
    for match_ in matches:
        file.write(match_ + "\n")