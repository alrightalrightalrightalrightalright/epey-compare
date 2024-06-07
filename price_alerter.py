import asyncio
import csv
import datetime
import logging
import random
from datetime import datetime

import cloudscraper
from bs4 import BeautifulSoup
from tqdm.auto import tqdm

import extras
import Item
# url = input("karşılaştırılacak epey linki: ")
from logging_config import configure_logging

url = "https://www.epey.com/akilli-telefonlar/karsilastir/716503-802356/apple-iphone-13_apple-iphone-14-pro/"
import time
import winsound

import httpx


def alert_beep(duration_ms=1000, frequency=440):
    winsound.Beep(frequency, duration_ms)
    time.sleep(duration_ms / 1000)


configure_logging()
logging.getLogger("data").info(f"price_1, price_2, timestamp")


def create_session():
    chosen_agent = random.choice(extras.POSSIBLE_AGENTS)
    ses = httpx.AsyncClient(headers=chosen_agent)
    return ses


PRICE_1_LIMIT = 56500
PRICE_2_LIMIT = 36500


def scrape():
    scraper = cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "windows", "mobile": False}
    )
    i = 0

    while True:
        print(f"runnin {i}")
        i = i + 1
        response = scraper.get(url)
        content = BeautifulSoup(response.text, features="lxml")

        price_1, price_2 = [
            float(x["data-sort"]) / 100
            for x in content.select(
                'div[id="sutun"] > a:first-child  span[class*="urun_fiyat"]'
            )
        ]
        logging.getLogger("data").info(f"{price_1}, {price_2}, {datetime.now()}")
        logging.info(f"{price_1}, {price_2}, {datetime.now()}")

        if price_1 < PRICE_1_LIMIT or price_2 < PRICE_2_LIMIT:
            print("AYOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
            time.sleep(1)
        #            while True:
        #                alert_beep()
        #                break
        time.sleep(30)


while True:
    try:
        scrape()
    except BaseException as ex:
        print(f"fukin error: {ex}")
        time.sleep(10)
