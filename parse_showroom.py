from selenium import webdriver
from telegram import Bot
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()


def send_message(bot, text):
    bot.send_message(chat_id=user_chat_id, text=text)


user_chat_id = os.getenv('USER_CHAT_ID')
token = os.getenv('BOT_TOKEN')
bot = Bot(token=token)
bot.send_message(chat_id=user_chat_id, text='bot is working')
while True:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(
        executable_path=os.environ.get("CHROMEDRIVER_PATH"),
        chrome_options=chrome_options)
    browser.get(
        'https://showroom.hyundai.ru/')
    soup = BeautifulSoup(browser.page_source, 'lxml')
    cars = soup.find_all(class_='car-item__wrap')
    for car in cars:
        car_brand = car.find(class_='text-uppercase').text
        car_price = car.find(class_='car-item__price-top').text
        car_engine = car.find_all(class_='mt-8')[1].find(class_='title').text
        text = f'''Автомобиль - Hyundai {car_brand}\nЦена - {car_price}\nДвигатель - {car_engine}'''
        if car_brand == 'Новая ELANTRA' or car_brand == 'Tucson':
            send_message(bot, text=text)
    browser.quit()
    time.sleep(80)
