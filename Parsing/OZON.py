import json
import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

#функция списана из видео -- пока не работает, видимо на озоне что-то поменяли с тех пор
def get_products_links(item_name='каска туристическая'):
    driver = uc.Chrome()
    driver.implicitly_wait(5)
    driver.get(url='https://ozon.ru')
    time.sleep(2)

    find_input = driver.find_element(By.NAME, 'text')
    find_input.clear()
    find_input.send_keys(item_name)
    time.sleep(2)

    find_input.send_keys(Keys.ENTER)
    time.sleep(2)

    current_url = f'{driver.current_url}'
    driver.get(url=current_url)
    time.sleep(2)

    try:
        find_links = driver.find_elements(By.CLASS_NAME,'tile-hover-target')
        products_urls = list(set([f'{link.get_attribute("href")}' for link in find_links]))
        print('Ссылки на товары собраны')
        print(products_urls)
    except Exception:
        products_urls = []
        print('Что-то пошло не так')

    products_dict = {}
    for k, v in enumerate(products_urls):
        products_dict.update({k:v})

    with open('products_urls_dict.json', 'w', encoding='utf-8') as f:
        json.dump(products_dict, f, indent=4, ensure_ascii=False)
    driver.close()
    driver.quit()

def main():
    get_products_links()

if __name__ == '__main__':
    main()