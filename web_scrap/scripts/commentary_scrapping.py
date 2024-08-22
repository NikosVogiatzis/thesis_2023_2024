# In this file the data retreival is being implemented. From file web_scrap/txt_files/urls.txt, we access each page refering to live commenteries of champions league game
# based on the tags (that found via page inspect) we extract all valueable information in the format: 'Minute' 'Event' and store them line by line in the file
# web_scrap/txt_files/commentary.txt 

import requests
from bs4 import BeautifulSoup


urls_from_file = []
file_path = 'web_scrap/txt_files/urls.txt'


urls = []
file_path = 'web_scrap/txt_files/urls.txt'


with open(file_path, 'r', encoding="utf-8") as file:
    for line in file:
        urls.append(line.strip())

matches = []

for ur_l in urls:

    url_1 = ur_l
    page = requests.get(url_1)
    soup1 = BeautifulSoup(page.content, 'html.parser')
    element_text = soup1.title.string
    if element_text != '':
        text = element_text.replace("Live Text Updates:", "")
        text = text.replace(" - Sports Mole", "").strip()
        matches.append(text)
    else:
        print('Element not found')

with open("web_scrap/txt_files/matches.txt", "w", encoding="utf-8") as file:
    for match_ in matches:
        file.write(match_ + "\n")


with open(file_path, 'r') as file:
    for line in file:
        urls_from_file.append(line.strip())


all_time_stamps = []
all_commentaries = []

index = 0

for url in urls_from_file:

    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    # Find all elements with class name specified and store them inside doc list
    url_elements = soup.find_all(class_=["b8b w100 even", "b8b w100 odd"])

    trimmed_time = []
    trimmed_commentary = []

    for element in url_elements:
        time_element = element.find(class_=["liveTime lc_text_t liveTxt", "liveTime lc_text_t red" ])
        if time_element:
            span_element = time_element.find('span', class_=['bold vertical pl8', 'bold vertical pl4'])
            # Extract the text from the <span> element
            time_text = span_element.text.strip()
            trimmed_time.append("MATCH_" + str(index) + " " + time_text)

        commentary_element = element.find(class_=['lc_text_x odd', 'lc_text_x even'])
        if commentary_element:
            span_element = commentary_element.find('span', class_='vertical')
            # Extract the text from the <span> element
            commentary_text = span_element.text.strip()
            trimmed_commentary.append(commentary_text)

    all_time_stamps.append(trimmed_time)
    all_commentaries.append(trimmed_commentary)

    index += 1

with open('web_scrap/txt_files/commentary.txt', 'w', encoding='utf-8') as file:
        for times, commentaries in zip(all_time_stamps, all_commentaries):
            for time, commentary in zip(times, commentaries):
                file.write(f"{time}\t{commentary}\n")

