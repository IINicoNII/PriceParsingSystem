import requests
from bs4 import BeautifulSoup

URL = "https://www.ozon.ru/product/samsung-smartfon-galaxy-s23-ultra-sm-s918n100-podderzhka-russkogo-yazyka-1sim-karta-12-512-1758923870/?at=PjtJzrWB8cJJ8G34I7M7JWYTn61qOgsnnZLLgTYwG2N&keywords=samsung+s23+ultra"
response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.prettify())