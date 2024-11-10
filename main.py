import requests  # pip install requests
from bs4 import BeautifulSoup  # pip install bs4
import random

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


url = 'https://www.vsemayki.ru/catalog/group/tableware_krujka?page=2&scroll=true'
headers = {
    'User-Agent': get_random_user_agent(),
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'  # Исправлено здесь
}
data = requests.get(url, headers=headers).text
block = BeautifulSoup(data, 'lxml')
heads = block.find('div', {'class': 'styles_catalog_list__21cuV'}).find_all('div', {
    'class': 'styles_catalog_list_card__3cP7c'})
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
    # params = loom.find('ul', {'class': 'styles_info__stats__2lM52'}).find_all('li')
    # for param in params:
    #     cerr = param.find_all('div', {'class': 'styles_stats__left__2V73H'})
    #     for key in cerr:
    #         print(key.text.strip())
    #         get_key = key.text.strip()
    #     berr = param.find_all('span', {'class': 'styles_stats__value__39GTP'})
    #     for value in berr:
    #         print(value.text.strip())
    #         get_value = value.text.strip()
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
    for item in result:
        print(item)
    photo = loom.find('div', {'class': 'styles_imagewrap__1UxKt'}).find('img')['src']
    print(photo)
    print('\n')
