import requests  # pip install requests
from bs4 import BeautifulSoup  # pip install bs4
import random
import json
import os

from unicodedata import category

# pip install lxml


# Список пользовательских агентов
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/113.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/112.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Mobile Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 OPR/76.0.4017.177',
    'Mozilla/5.0 (Linux; Android 11; Pixel 4 XL Build/RQ3A.210705.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
    'Mozilla/5.0 (Linux; Android 5.1; Nexus 5 Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Mobile Safari/537.36'
]


# Функция для получения случайного пользовательского агента
def get_random_user_agent():
    return random.choice(user_agents)


count = 1
while True:
    url = f'https://www.vsemayki.ru/catalog/group/woman_tshirts?page={count}&scroll=true'
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'  # Исправлено здесь
    }
    data = requests.get(url, headers=headers).text
    block = BeautifulSoup(data, 'lxml')
    category = block.find('h1', {'itemprop': 'name'}).text.strip()
    print(category)
    heads = block.find('div', {'class': 'styles_catalog_list__21cuV'}).find_all('div', {
        'class': 'styles_catalog_list_card__3cP7c'})
    if not heads:  # Stop if no items found
        print("No more items found.")
        break
    print(len(heads))
    for head in heads:
        link = 'https://www.vsemayki.ru' + head.find('a')['href']
        print(link)
        soup = requests.get(link, headers=headers).text.strip()
        loom = BeautifulSoup(soup, 'lxml')
        name = loom.find('h1', {'itemprop': 'name'}).text.strip()
        print(name)
        price = loom.find('span', {'class': 'style_price__rHMRx'}).text.strip().replace('₽', '')
        print(price)
        articul = loom.find('span', {'class': 'styles_code__pAr2X'}).text.strip()
        print(articul)
        discription = loom.find('p', {'itemprop': 'description'}).text.strip()
        print(discription)
        params = loom.find('ul', {'class': 'styles_info__stats__2lM52'}).find_all('li')
        result = []
        for param in params:
            cerr = param.find_all('div', {'class': 'styles_stats__left__2V73H'})
            berr = param.find_all('span', {'class': 'styles_stats__value__39GTP'})

            for key, value in zip(cerr, berr):
                get_key = key.text.strip()
                get_value = value.text.strip()

                # Concatenate key and value and store in the result list
                result.append(get_key + ": " + get_value)  # You can choose your preferred format

        # Output the results
        foto = []
        for item in result:
            print(item)
        photo = loom.find('img', class_='styles_main__2tpaj')
        if photo:
            src_value = photo.get('src')
            print(src_value)
            foto.append(src_value)
        else:
            print("Элемент не найден")
        print('\n')

        # storage = {'name': name, 'price': price, 'articul': articul, 'discription': discription, 'params': result, 'foto': foto}
        # Создание словаря
        storage = {
            'category': category,
            'name': name,
            'price': price,
            'articul': articul,
            'discription': discription,
            'params': result,
            'foto': foto
        }

        # Файл для хранения данных
        file_path = f'{category}.json'

        # Проверяем, существует ли файл, и считываем существующие данные, если они есть
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as json_file:
                try:
                    existing_data = json.load(json_file)
                    if isinstance(existing_data, list):  # Если данные уже в виде списка
                        existing_data.append(storage)  # Добавляем новый объект
                    else:
                        existing_data = [existing_data, storage]  # Создаем список
                except json.JSONDecodeError:
                    existing_data = [storage]  # Ошибка чтения, создаем новый список
        else:
            existing_data = [storage]  # Файла нет, создаем новый список

        # Запись обновленных данных обратно в файл
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, ensure_ascii=False, indent=4)
    count += 1
    print('Page_num:' + str(count))
