import urllib.parse
from bs4 import BeautifulSoup
import requests
from config import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

URL = "https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22north%22%3A37.93143513338194%2C%22east%22%3A-122.27831927661133%2C%22south%22%3A37.6188183009402%2C%22west%22%3A-122.58833972338867%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%7D"
base = "https://www.zillow.com"

response = requests.get(URL, headers={'Accept-Language': 'en-US,en;q=0.9',
                                      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'})

zillow_web_page = response.text

soup = BeautifulSoup(zillow_web_page, "html.parser")

listings = soup.find_all(name="article", class_="list-card_for-rent")

links = []
addresses = []
prices = []
for listing in listings:
    link = listing.find(name="a", href=True).get("href")
    link = urllib.parse.urljoin(base, link)
    links.append(link)
    address = listing.find(name="address").get_text()
    addresses.append(address)
    price = listing.find(name="span").get_text()[:6]
    prices.append(price)

print(f"Links {links}")
print(f"Addresses {addresses}")
print(f"Prices {prices}")

links = links_list
addresses = addresses_list
prices = prices_list

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

driver.get(FORM_URL)

for i in range(0, len(links)):
    address_input = driver.find_element(By.XPATH,
                                        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_input.send_keys(addresses[i])
    price_input = driver.find_element(By.XPATH,
                                      '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input.send_keys(prices[i])
    link_input = driver.find_element(By.XPATH,
                                     '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input.send_keys(links[i])

    submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit.click()

    new_entry = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    new_entry.click()

driver.close()
