from pathlib import Path
import requests
from bs4 import BeautifulSoup
from datetime import date
import re
import hashlib


def make_request(url):
    session = requests.session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15'}
    response = session.get(url, headers=headers)
    response.raise_for_status()
    return response


def extract_data(html):
    data = ""
    today = date.today().strftime("%Y-%m-%d")

    categories_html = html.find('ul', {"style": "padding-left:17px;"})
    items = categories_html.find_all("li", {"class": "item"})

    for item in items:
        itemLinkH2 = item.find('h2', {"class": "more"})
        itemLink = ''

        for tag in itemLinkH2.findAll("a", href=True):
            itemLink = tag['href']

        PublishedDate = re.sub(' +', ' ', item.find('div', {"class": "s"}).text).strip()
        # Skip records that don't have the current date
        if PublishedDate != today:
            continue

        Name = item.find('h2', {"class": "more"}).text
        itemImage = item.find('div')
        itemImageLink = ''
        for tag in itemImage.findAll("a", href=True):
            if img := tag.img:
                itemImageLink = 'https:' + img.get("src")

        Location = re.sub(' +', ' ', item.find('div', {"class": "boxintxt"}).text).strip()
        Price = re.sub(' +', ' ', item.find('div', {"class": "b"}).text).strip()

        itemDetails = item.find('div', {"class": "boxtext"}).text
        itemDetailsArr = itemDetails.split()
        Milage = itemDetailsArr[3] if len(itemDetailsArr) == 6 else itemDetailsArr[2]

        item_hash = hashlib.md5(
            (Name + itemLink + itemImageLink + Location + Price + Milage + PublishedDate).encode()
        ).hexdigest()

        data += f"""
<!-- {item_hash} -->

### [{Name}]({itemLink})

![{Name}]({itemImageLink})

Location: **{Location}**

Price (Rs): **{Price}**

Mileage (Km): **{Milage}**

Publish Date: **{PublishedDate}**

"""

    return data


def save_to_markdown(data, file_path):
    with open(file_path, "w") as data_file:
        data_file.write(data)


def read_existing_data(file_path):
    with open(file_path, "r") as data_file:
        return data_file.read()


def main():
    base_url = "https://riyasewana.com/search/cars/toyota/vitz"
    filtered_url = base_url + ""

    try:
        response = make_request(filtered_url)
        html = BeautifulSoup(response.text, 'html.parser')
        new_data_markdown = extract_data(html)

        existing_data = read_existing_data("data.md")
        existing_hashcodes = re.findall(r'<!-- (.*?) -->', existing_data)

        new_hashcodes = re.findall(r'<!-- (.*?) -->', new_data_markdown)

        if set(existing_hashcodes) == set(new_hashcodes):
            print("No new items found. Skipping update.")
            return

        save_to_markdown(new_data_markdown, "data.md")
    except requests.exceptions.RequestException as e:
        print("Error making the request:", e)
    except Exception as e:
        print("An error occurred:", e)


if __name__ == '__main__':
    main()
