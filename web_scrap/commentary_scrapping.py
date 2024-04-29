import requests
from bs4 import BeautifulSoup


urls_from_file = []
file_path = 'urls.txt'

# -------- Read the urls via output.txt file --------

with open(file_path, 'r') as file:
    for line in file:
        urls_from_file.append(line.strip())

# ---------- end of reading ----------

# -> extract commentary and store them 


all_times = []
all_commentaries = []

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

            trimmed_time.append(time_text)

        commentary_element = element.find(class_=['lc_text_x odd', 'lc_text_x even'])
        if commentary_element:
            span_element = commentary_element.find('span', class_='vertical')
            # Extract the text from the <span> element
            commentary_text = span_element.text.strip()

            trimmed_commentary.append(commentary_text)

    all_times.append(trimmed_time)
    all_commentaries.append(trimmed_commentary)

    # Open the file in write mode
with open('commentary.txt', 'w', encoding='utf-8') as file:
        for times, commentaries in zip(all_times, all_commentaries):
            for time, commentary in zip(times, commentaries):
                file.write(f"{time}\t{commentary}\n")
