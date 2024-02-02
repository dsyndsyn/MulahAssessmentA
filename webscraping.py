import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from urllib.parse import urljoin
import json

def fetch_and_save_theverge_headlines():
    url = 'https://www.theverge.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    article_elements = soup.find_all('h2', class_='font-polysans text-20 font-bold leading-100 tracking-1 md:text-24 lg:text-20')

    headlines = []

    for idx, article_element in enumerate(article_elements, 1):
        title_element = article_element.find('a')
        title = title_element.text.strip()
        link = urljoin(url, title_element['href'])  # Convert the relative link to absolute
        pub_date_str = article_element.find_next('time')['datetime']

        pub_date = datetime.strptime(pub_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')

        pub_date = pub_date.replace(tzinfo=timezone.utc)

        # Check article from 1st January 2024 onwards
        if pub_date >= datetime(2024, 1, 1, tzinfo=timezone.utc):
            headlines.append({"title": title, "link": link, "pub_date": pub_date.isoformat()})
        else:
            print(f"Article {idx} skipped. Published on {pub_date.isoformat()}.")

    # Save to a JSON file
    with open('titles.json', 'w') as json_file:
        json.dump(headlines, json_file, indent=2)

    print(json.dumps(headlines, indent=2))

fetch_and_save_theverge_headlines()