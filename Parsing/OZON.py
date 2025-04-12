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

# получить информацию по ссылке
def get_info_by_url(driver, url):
    time.sleep(3)
    driver.get(url)
    time.sleep(3)
    output_dict = {}
    product_id = driver.find_element(By.XPATH, '//div[contains(text(), "Артикул: ")]').text.split('Артикул: ')[1]

    page_source = str(driver.page_source)
    soup = BeautifulSoup(page_source, 'lxml')
    product_name = soup.find('div', attrs={"data-widget":'webProductHeading'}).find('h1').text.strip().replace('\t','').replace('\n',' ')
    try:
        ozon_card_price_elem = soup.find('span', string='с Ozon Картой').parent.find('div').find('span')
        price_ozon_card = ozon_card_price_elem.text.strip() if ozon_card_price_elem else ''
        price_elem = soup.find('span', string='без Ozon Карты').parent.parent.find('div').findAll('span')
        price_discount = price_elem[0].text.strip() if price_elem[0] else ''
        price_base = price_elem[1].text.strip() if price_elem[1] is not None else ''
    except:
        price_ozon_card = None
        price_discount = None
        price_base = None

    try:
        soup.find('span', string='с Ozon Картой').parent.find('div').find('span')
    except AttributeError:
        card_price_div = soup.find('div', attrs={'data-widget':'webPrice'}).findAll('span')
        price_base = card_price_div[0].text.strip()
        price_discount = card_price_div[1].text.strip()


    output_dict['Артикул'] = product_id
    output_dict['Название'] = product_name
    output_dict['Базовая цена'] = price_base
    output_dict['Цена со скидкой'] = price_discount
    output_dict['Цена по карте'] = price_ozon_card
    return output_dict

# получить информацию по артикулу
def get_info_by_id(driver, product_id):
    pass

def main():
    driver = uc.Chrome()
    driver.implicitly_wait(5)
    url = 'https://www.ozon.ru/product/bioherb-kokosovye-slivki-suhie-rastitelnye-250-g-761091846/?at=BrtzW6wkQuNpXKPqT77jox1cvM2p3AHWvlnKphJ7roOm&keywords=%D1%81%D1%83%D1%85%D0%BE%D0%B5+%D0%BA%D0%BE%D0%BA%D0%BE%D1%81%D0%BE%D0%B2%D0%BE%D0%B5+%D0%BC%D0%BE%D0%BB%D0%BE%D0%BA%D0%BE'
    output = get_info_by_url(driver, url)
    print(output)

if __name__ == '__main__':
    main()