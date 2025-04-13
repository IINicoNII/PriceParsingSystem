import json
import time
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class OzonParser:
    def __init__(self):
        self.driver = uc.Chrome()
        self.driver.implicitly_wait(5)

    def create_driver(self):
        self.driver = uc.Chrome()
        self.driver.implicitly_wait(5)

    def close_driver(self):
        self.driver.quit()

    #функция списана из видео -- пока не работает, видимо на озоне что-то поменяли с тех пор
    def get_products_links(self, item_name='каска туристическая'):
        self.create_driver()
        self.driver.get(url='https://ozon.ru')
        time.sleep(2)

        find_input = self.driver.find_element(By.NAME, 'text')
        find_input.clear()
        find_input.send_keys(item_name)
        time.sleep(2)

        find_input.send_keys(Keys.ENTER)
        time.sleep(2)

        current_url = f'{self.driver.current_url}'
        self.driver.get(url=current_url)
        time.sleep(2)

        try:
            find_links = self.driver.find_elements(By.CLASS_NAME,'tile-hover-target')
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
        self.close_driver()

    def extract_info(self):
        page_source = str(self.driver.page_source)
        soup = BeautifulSoup(page_source, 'lxml')
        product_name = soup.find('div', attrs={"data-widget": 'webProductHeading'}).find('h1').text.strip().replace('\t',
                                                                                                                    '').replace(
            '\n', ' ')
        try:
            ozon_card_price_elem = soup.find('span', string='c Ozon Картой').parent.find('div').find('span')
            price_ozon_card = ozon_card_price_elem.text.strip() if ozon_card_price_elem else ''
            price_elem = soup.find('span', string='без Ozon Карты').parent.parent.find('div').find_all('span')
            price_discount = price_elem[0].text.strip() if price_elem[0] else ''
            price_base = price_elem[1].text.strip() if price_elem[1] is not None else ''
        except:
            price_ozon_card = None
            price_discount = None
            price_base = None

        try:
            soup.find('span', string='c Ozon Картой').parent.find('div').find('span')
        except AttributeError:
            card_price_div = soup.find('div', attrs={'data-widget': 'webPrice'}).find_all('span')
            price_base = card_price_div[0].text.strip()
            price_discount = card_price_div[1].text.strip()

        output_dict = dict()
        output_dict['Название'] = product_name
        output_dict['Базовая цена'] = int(price_base.replace('\u2009','')[:-1])
        output_dict['Цена со скидкой'] = int(price_discount.replace('\u2009','')[:-1])
        output_dict['Цена по карте'] = int(price_ozon_card.replace('\u2009','')[:-1])
        return output_dict

    # получить информацию по ссылке
    def get_info_by_url(self, url):
        self.create_driver()
        time.sleep(3)
        self.driver.get(url)
        time.sleep(3)
        product_id = self.driver.find_element(By.XPATH, '//div[contains(text(), "Артикул: ")]').text.split('Артикул: ')[1]
        output_dict = self.extract_info()
        output_dict['Артикул'] = int(product_id)
        self.close_driver()
        return output_dict

    # получить информацию по артикулу
    def get_info_by_id(self, product_id):
        self.driver.get(url='https://ozon.ru')
        time.sleep(5)

        find_input = self.driver.find_element(By.NAME, 'text')
        find_input.clear()
        find_input.send_keys(str(product_id))
        time.sleep(5)

        find_input.send_keys(Keys.ENTER)
        time.sleep(5)

        output_dict = self.extract_info()
        output_dict['Артикул'] = int(product_id)
        return output_dict


def main():
    parser = OzonParser()
    try:
        output = parser.get_info_by_id(1280883309)
        print(output)
    finally:
        parser.close_driver()

if __name__ == '__main__':
    main()