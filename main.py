import json
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from datetime import date
import re


def make_request(url):
    session = requests.session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15'}
    response = session.get(url, headers=headers)
    response.raise_for_status()
    cookies = requests.utils.dict_from_cookiejar(session.cookies)
    Path("cookies.json").write_text(json.dumps(cookies))
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
                itemLink =tag['href']
                
        PublishedDate = re.sub(' +', ' ', item.find('div', {"class": "s"}).text).strip()
       # Skip records that don't have the current date
        if PublishedDate != today:
            continue

        Name = item.find('h2', {"class": "more"}).text
        itemImage = item.find('div')
        itemImageLink = ''
        for tag in itemImage.findAll("a", href=True):
            if img := tag.img:
                itemImageLink = 'https:'+img.get("src")

        Location = re.sub(' +', ' ', item.find('div', {"class": "boxintxt"}).text).strip()
        Price = re.sub(' +', ' ', item.find('div', {"class": "b"}).text).strip()

        itemDetails = item.find('div', {"class": "boxtext"}).text
        itemDetailsArr = itemDetails.split()
        Milage = itemDetailsArr[3] if len(itemDetailsArr) == 6 else itemDetailsArr[2]

       
       


        data += """
##        
### [{}]({})

![{}][{}]

Location: **{}**

Price (Rs): **{}**

Mileage (Km): **{}**

Publish Date: **{}**

""".format(Name,itemLink,Name,itemImageLink,Location,Price,Milage,PublishedDate)

    return data


def save_to_markdown(data, file_path):
    with open(file_path, "w") as data_file:
        data_file.write(data)


def main():
    base_url = "https://riyasewana.com/search/cars/toyota/vitz"
    filtered_url = base_url + ""

    try:
        response = make_request(filtered_url)
        html = BeautifulSoup(response.text, 'html.parser')
        data_markdown = extract_data(html)
        save_to_markdown(data_markdown, "data.md")
    except requests.exceptions.RequestException as e:
        print("Error making the request:", e)
    except Exception as e:
        print("An error occurred:", e)


if __name__ == '__main__':
    main()
