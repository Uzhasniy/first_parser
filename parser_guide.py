from random import random, randrange
from time import sleep
import requests
from bs4 import BeautifulSoup as BS
import json
import csv

# url ="https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0"
}
# req = requests.get(url, headers=headers)
# src = req.text

# with open("index.html", "w", encoding='utf=8') as file:
#     file.write(src)

# with open("index.html", encoding='utf=8') as file:
#     src = file.read()

# soup = BS(src, "lxml")
# all_prod_href  = soup.find_all(class_="mzr-tc-group-item-href")

# all_catagories = {}
# for item in all_prod_href:
#     item_text = item.text
#     item_href = "https://health-diet.ru" + item.get("href")

#     all_catagories[item_text]  = item_href

# with open("all_catagories.json","w", encoding='utf=8') as file:
#     json.dump(all_catagories, file, indent=4, ensure_ascii=False)
with open("all_catagories.json", encoding='utf=8') as file:
    all_catagories = json.load(file)

iteration_count = int(len(all_catagories)) - 1
count = 0
print(f"Всего итераций: {iteration_count}")

for category_name, category_href in all_catagories.items():

    rep = [",", " ", "-", "'"]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, "_")
    
    req = requests.get(url=category_href, headers=headers)
    src = req.text

    with open(f"data/{count}_{category_name}.html","w", encoding='utf=8') as file:
        file.write(src)

    with open(f"data/{count}_{category_name}.html", encoding='utf=8') as file:
        src = file.read()

    soup = BS(src,"lxml")

    #наличие таблицы
    alert_block = soup.find(class_= "uk-alert-danger")
    if alert_block is not None:
        continue

    #заголовки сбор
    table_head = soup.find(class_="mzr-tc-group-table").find("tr").find_all("th")
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carb = table_head[4].text
    
    with open(f"data/{count}_{category_name}.csv","w", encoding='utf=8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fats,
                carb
            )
        )

    #собираем данные
    product_data = soup.find(class_="mzr-tc-group-table").find("tbody").find_all("tr")

    product_info = []
    for item in product_data:
        prod_tds = item.find_all("td")

        title = prod_tds[0].find("a").text
        calories = prod_tds[1].text
        proteins = prod_tds[2].text
        fats = prod_tds[3].text
        carb = prod_tds[4].text

        product_info.append(
            {
                "Title": title,
                "Calories": calories,
                "Proteins": proteins,
                "Fats": fats,
                "Carb": carb,
            }
        )

        with open(f"data/{count}_{category_name}.csv","a", encoding='utf=8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fats,
                    carb
                )
            )

    with open(f"data/{count}_{category_name}.json","a", encoding='utf=8') as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)

    count+=1
    print(f"Итерация {count}. {category_name} записан...")
    iteration_count = iteration_count - 1

    if iteration_count == 0:
        print("Работа завершена")
        break

    print(f"Осталось итераций: {iteration_count}")
    # sleep(randrange(1,2))