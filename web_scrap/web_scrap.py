import requests
from bs4 import BeautifulSoup

url = 'https://www-sportsmole-co-uk.translate.goog/football/champions-league/results.html?_x_tr_sl=en&_x_tr_tl=el&_x_tr_hl=el&_x_tr_pto=sc'

page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

# Find all elements with class name specified and store them inside doc list
url_elements = soup.find_all(class_='l_sfp_links')

# Here all urls from which we want to extract data, are stored
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

# Write all urls in the file urs.txt

file_path = "urls.txt"


# Open the file in write mode
with open(file_path, 'w') as file:
    # Iterate over the elements of the list
    for item in links_to_commentary:
        # Write each element followed by a newline character
        file.write(item + '\n')

# Initialize an empty list to store the lines
