# This script is responsible for extracting the url's from 30 latest match results for champions league
# it is implemented with BeautifulSoup 
# after retrieving the urls, they get saved in a file urls.txt in directory web_scrap/txt_files/
# i also extract the match name (basically the result form Live Updates title) and store each match result 
# in a file matches.txt (e.g: Borussia Dortmund 0 - 2 Real Madrid). I do that so that when i implement the ner and relationships extractions. 
# each even should get associated with the match that it took place

import requests
from bs4 import BeautifulSoup

url = "https://www.sportsmole.co.uk/football/champions-league/results.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

# Find all elements with class name specified and store them inside doc list
url_elements = soup.find_all(class_='l_sfp_links')
urls = []

# for each element inside url_elements, grab the href to match details url
ind = 0
for element in url_elements:
    if ind == 30:
        break
    if 'href' in element.attrs:
        href = "https://www.sportsmole.co.uk/"+element['href']
        urls.append(href)
    ind = ind + 1

# Find all tags that contain the href link to the page containing the live commentary
links_to_commentary = []
for ur_l in urls:
    url_1 = ur_l
    page1 = requests.get(url_1)
    soup1 = BeautifulSoup(page1.content, 'html.parser')
    tag = soup1.find('a', href=lambda x: x and 'live-updates' in x)
    wanted_url = tag['href']
    wanted_url_to_comm = "https://www.sportsmole.co.uk" + wanted_url
    links_to_commentary.append(wanted_url_to_comm)

matches = []
for ur_l in links_to_commentary:
    url_1 = ur_l
    page = requests.get(url_1)
    soup1 = BeautifulSoup(page.content, 'html.parser')
    element = soup1.find('h1', {'id': 'title_text_wide', 'itemprop': 'headline'})
    if element:
        text = element.get_text(strip=True).replace("Live Updates:", "")
        matches.append(text)
    else:
        print('Element not found')
        exit

# Write all urls in the file urls.txt and matches titles in matches.txt
file_path = "web_scrap/txt_files/urls.txt"
with open(file_path, 'w') as file:
    for item in links_to_commentary:
        file.write(item + '\n')
 
with open("web_scrap/txt_files/matches.txt", "w", encoding="utf-8") as file:
    for match_ in matches:
        file.write(match_ + "\n")






