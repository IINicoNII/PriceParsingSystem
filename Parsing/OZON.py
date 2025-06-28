import tempfile
import shutil
import random
import time
import json
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import selenium_stealth
from pyvirtualdisplay import Display

class OzonParser:
    def __init__(self):
        self.display = Display(visible=0, size=(1920, 1080))
        self.display.start()
        self.temp_dir = tempfile.mkdtemp()
        self.driver = self.create_driver()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_driver()
        return False

    def create_driver(self):
        options = Options()

        # 🔹 Уникальный каталог для данных пользователя
        options.add_argument(f"--user-data-dir={self.temp_dir}")

        # 🔹 Основные настройки
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-automation")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--dns-prefetch-disable")
        options.add_argument("--lang=en-US")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        driver = webdriver.Chrome(options=options)

        selenium_stealth.stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        return driver

    def close_driver(self):
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None

        if self.display:
            try:
                self.display.stop()
            except:
                pass

        if self.temp_dir:
            try:
                shutil.rmtree(self.temp_dir, ignore_errors=True)
            except:
                pass

    #функция списана из видео -- пока не работает, видимо на озоне что-то поменяли с тех пор
    def get_products_links(self, item_name='каска туристическая'):
        #self.display.start()
        self.create_driver()
        self.driver.get(url='https://ozon.ru')
        time.sleep(random.uniform(1, 3))

        find_input = self.driver.find_element(By.NAME, 'text')
        find_input.clear()
        find_input.send_keys(item_name)
        time.sleep(random.uniform(1, 3))

        find_input.send_keys(Keys.ENTER)
        time.sleep(random.uniform(1, 3))

        current_url = f'{self.driver.current_url}'
        self.driver.get(url=current_url)
        time.sleep(random.uniform(1, 3))

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
        #self.display.stop()

    def __del__(self):
        self.close_driver()

    def extract_info(self):
        print('extracting info...')
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
        try:
            self.driver.get(url)
            time.sleep(random.uniform(2, 4))
            product_id = self.driver.find_element(By.XPATH, '//div[contains(text(), "Артикул: ")]').text.split('Артикул: ')[1]
            output_dict = self.extract_info()
            output_dict['Артикул'] = int(product_id)
            return output_dict
        except Exception as e:
            print(f"Ошибка при получении данных по URL: {e}")
            return {}

    # получить информацию по артикулу
    def get_info_by_id(self, product_id):
        try:
            self.driver.get('https://ozon.ru')
            time.sleep(random.uniform(3, 5))

            find_input = self.driver.find_element(By.NAME, 'text')
            find_input.clear()
            find_input.send_keys(str(product_id))
            time.sleep(random.uniform(1, 2))

            # Имитация человеческих действий
            action = ActionChains(self.driver)
            for _ in range(2):
                action.move_by_offset(
                    random.randint(10, 30),
                    random.randint(10, 30)
                ).perform()
                time.sleep(random.uniform(0.1, 0.3))

            find_input.send_keys(Keys.ENTER)
            time.sleep(random.uniform(3, 5))

            output_dict = self.extract_info()
            output_dict['Артикул'] = int(product_id)
            return output_dict
        except Exception as e:
            print(f"Ошибка при получении данных по артикулу {product_id}: {e}")
            return {}


def main():
    parser = OzonParser()
    try:
        output = parser.get_info_by_id(1821495135)
        print(output)
    finally:
        parser.close_driver()

if __name__ == '__main__':
    main()