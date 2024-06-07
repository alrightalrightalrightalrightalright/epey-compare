
import cloudscraper
from bs4 import BeautifulSoup

url = "https://www.epey.com/kulaklik/qcy-t13-anc.html"


import logging



def configure_logging():
    # Keep the basicConfig call
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s(%(levelname)s)[%(threadName)s]: %(message)s",
        datefmt="%d.%m.%Y %I:%M:%S"
    )

    # Configure the existing StreamHandler
    console_handler = logging.getLogger().handlers[0]
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s(%(levelname)s)[%(threadName)s]: %(message)s", "%d.%m.%Y %I:%M:%S"
    )
    console_handler.setFormatter(formatter)


def scrape():
    scraper = cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "windows", "mobile": False}
    )
    logging.info(f"runnin")

    response = scraper.get(url)
    content = BeautifulSoup(response.text, features="lxml")

    prices = content.select('div[class*="fiyat"] > a')
    logging.info(f"{len(prices)} sellers exist")
    for price in prices:
        seller_text = price.select_one('span[class*="urun_adi"] p')
        if seller_text:
            seller = seller_text.contents[1].get_text().replace("|", "").strip()
            if seller.lower() != "mobiletrend":
                print("AYOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        else:
            seller=""
        price_text = (
            price.select_one('span[class*="urun_fiyat"]').contents[0]
            .get_text()
            .lower()
            .replace("tl", "")
            .strip()
        )
        price_val = float(price_text.replace(",", "."))
        logging.info(f"price: {price_val}\n")
        logging.info(f"seller: {seller}")

def lambda_handler(event, context):
    configure_logging()
    try:
        scrape()
    except BaseException as ex:
        logging.error(f"fukin error: {ex}")
