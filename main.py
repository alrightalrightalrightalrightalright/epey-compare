import asyncio
import csv
import datetime
import random
import re

import cloudscraper
from bs4 import BeautifulSoup
from tqdm.auto import tqdm

import extras
import Item
import pandas as pd

# url = input("karşılaştırılacak epey linki: ")
url = "https://www.epey.com/laptop/e/YToyOntzOjQ6Im96ZWwiO2E6MTp7aTowO3M6Nzoic2F0aXN0YSI7fXM6NToiZml5YXQiO2E6Mjp7aTowO3M6NDoiNDAwMCI7aToxO3M6NjoiMjE4MDAwIjt9fV9OOw==/"
import httpx


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


async def request_get_async(
    client: httpx.AsyncClient,
    url: str,
    follow_redirects: bool = False,
    get_response: bool = False,
    params: dict = None,
):
    attempts = 0
    error = None
    while attempts < 5:
        try:
            response = await client.get(
                url, follow_redirects=follow_redirects, params=params
            )
            if get_response:
                return response
            return BeautifulSoup(response.content, features="lxml")
        except httpx.HTTPError as e:
            await asyncio.sleep(2)
            attempts += 1
            error = e
    raise Exception(f"Too many failed attempts (async). Error: {error}")


file_name = ""
header = None


def clean_row(row):
    cleaned_row = []
    for cell in row:
        #cell = ' '.join(cell.split())

        if 'adi' in cell['class']:
            extra_attributes=  [x.get_text().strip() for x in cell .select('div[class="detay cell"] > span')]
            product_name = cell.select_one('a[class="urunadi"]').get_text().strip()
            extra_attributes.insert(0, product_name)
            cell = " | ".join(extra_attributes)
        elif 'fiyat' in cell['class']:
            cell  = (
                cell.select_one('a')
                .get_text()
                .replace(".", "")
                .split(",")[0])
        elif 'puan' in cell['class']:
            try:
                cell = cell.select_one('div')["data-percent"]
            except TypeError:
                cell = ""
        else:
            cell = cell.get_text().replace('\n', ' ').strip()
        #if depolama:
        #    kapasite_text = item.select_one('li[class*="adi cell"] span[class="aile"]').get_text().strip()
        #    numeric_part = int(re.search(r'\d+', kapasite_text).group())
        #    kapasite = 1024 * numeric_part if "TB" in kapasite_text else numeric_part

        cleaned_row.append(cell)
    return cleaned_row

def list_to_dict(row):
    return {f'col{i+1}': value for i, value in enumerate(row)}


async def get_page_details(client, page, progress, depolama=False):
    content = await request_get_async(client, page)

    final = []
    containers = content.select('ul[class="metin row"]')

    global header
    if header is None:
        header = [x.get_text().strip() for x in content.select('ul[class="baslik row"] li')]
        header.insert(0,"Link")
        #if 'Teknik Puan' in header:
        #    header.append('Wortluk')
        print('header set: ', header)

    for item in containers:
        try:
            if item.select_one('span[class="sponsormetni"]') or item.select_one('span:contains("Reklam")'):
                continue

            columns = [x for x in item.select('li')]
            print(f"cols length is {len(columns)} for url: {page} ")
            row = clean_row(columns)

            link = item.select_one('a[class="urunadi"]')["href"]
            row.insert(0,link)

            final.append(list_to_dict(row))

        except TypeError as ex:
            breakpoint()
        except BaseException as e:
            breakpoint()

    progress.update(1)
    return final


def create_session():
    chosen_agent = random.choice(extras.POSSIBLE_AGENTS)
    ses = httpx.AsyncClient(headers=chosen_agent)
    return ses


async def scrape():
    scraper = cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "windows", "mobile": False}
    )
    response = scraper.get(url)
    content = BeautifulSoup(response.text, features="lxml")
    last_page_index = int(
        content.select_one('a[class="son"]')["href"].strip("/").split("/")[-1]
    )
    pages = [f"{url.strip().strip('/')}/{x}/" for x in range(1, last_page_index + 1)]
    search_title = (
        content.select_one('div[id="ustbilgi"] h1').get_text().replace(" ", "_")
    )
    file_name = (
        f'{datetime.datetime.now().strftime("%m %d %Y_%H-%M-%S")}_{search_title}.csv'
    )
    progress = tqdm(
        total=len(pages),
        desc="sayfa",
        leave=False,
    )
    pieces = chunks(pages, 10)
    final = []
    for piece in pieces:
        async with create_session() as client:
            tasks = [get_page_details(client, page, progress) for page in piece]
            result = await asyncio.gather(*tasks)
            final.extend(sum(result, []))
    progress.close()


    df = pd.DataFrame(final)

    # Rename columns based on header
    df.columns = header

    # Create the 'wortluk' column
    if 'Teknik Puan' in header:
        df['wortluk'] = df.apply(
            lambda row: float(row['Fiyat']) / float(row['Teknik Puan']) if row['Teknik Puan'].strip() and row[
                'Fiyat'].strip() else '', axis=1)

    df.to_csv(file_name, index=False)

    return df


asyncio.run(scrape())
