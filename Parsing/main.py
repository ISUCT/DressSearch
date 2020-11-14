from bs4 import BeautifulSoup
import requests
import re

base_link = "https://www.lamoda.ru"
women_base = f"{base_link}/women-home/"
# man-home , kids-home

response = requests.get(women_base)

page_soup = BeautifulSoup(response.content, "html.parser")
items = ["Одежда", "Обувь"]
nav = page_soup.find("div", {"class" : "d-header-top-menu-wrapper"})
for item in items:
    element = nav.find_all("a", string=re.compile(f".*{item}"))
    
cloth_link = page_soup.find_all(string=re.compile(f".*Одежда"))
cloth_link = "/c/355/clothes-zhenskaya-odezhda"   #TODO - get it from link

clothes = requests.get(f"{base_link}{cloth_link}")
clothes_soup = BeautifulSoup(clothes.content, "html.parser")

cloth_nav = clothes_soup.find("ul", {"class": "js-outlet-icons-slider"})
clothes = cloth_nav.find_all("a")
for cloth in clothes:
    print(cloth.attrs["href"].split("aim=")[1])

clothes = requests.get(f"{base_link}/c/369/clothes-platiya/?page=1")
clothes_soup = BeautifulSoup(clothes.content, "html.parser")


import os
cloth_nav = clothes_soup.find("div", {"class": "products-catalog__list"})
clothes = cloth_nav.find_all("div", {"class": "products-list-item"})
for cloth in clothes: 
    images = cloth.attrs["data-gallery"].replace("[","").replace("]","").replace('"',"").split(",")
    sku = cloth.attrs["data-sku"]
    os.mkdir(f"temp/{sku}")
    i = 1
    for image in images:
        url = f"http:{image.strip()}"
        image = requests.get(url)
        file = open(f"temp/{sku}/{i}.jpg", "wb")
        file.write(image.content)
        file.close()
        i += 1