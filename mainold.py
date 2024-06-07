import requests
from bs4 import BeautifulSoup

url = "https://www.epey.com/laptop/e/YToyOntzOjQ6Im96ZWwiO2E6MTp7aTowO3M6Nzoic2F0aXN0YSI7fXM6NToiZml5YXQiO2E6Mjp7aTowO3M6MToiMyI7aToxO3M6NzoiMjA3NDAwMCI7fX1fczo5OiJmaXlhdDpBU0MiOw==/"
headers = {
    "Accept": "*/*",
    "Host": "www.epey.com",
    "Connection": "keep-alive",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.317",
}

# url = input("Lütfen karşılaştırılacak kategori linkini giriniz: ")
s = requests.Session()

r = s.get(url, headers=headers, timeout=None)
soup = BeautifulSoup(r.text, "html.parser")
pageCount = (
    soup.find("a", class_="son")["onclick"]
    .split(";")[0]
    .replace("sayfa(", "")
    .replace(")", "")
)
fileName = soup.find("div", class_="kategori_adi cell").h1.text
i = 1
while i <= int(pageCount):
    r = s.get(url + str(i), headers=headers, timeout=None)
    print("sayfa:", i, "/", pageCount, "   Get: ", r.status_code)

    soup = BeautifulSoup(r.text, "html.parser")
    containers = soup.find_all("ul", class_="metin row")

    for tel in containers:
        try:
            link = tel.find("li", class_="fiyat cell").a.get("href")
            # fiyat =tel.find("li",class_="fiyat cell").a.text.split()[0].replace(".","").split(",")[0] #tl
            fiyat = (
                tel.find("li", class_="fiyat cell")
                .a.text.split()[0]
                .replace(".", "")
                .split(",")[0]
            )  # tl
            puan = tel.find("li", class_="puan cell").div["data-text"]

            wortluk = int(fiyat) / int(puan)
            file = open(fileName + ".csv", "a", encoding="utf8")
            file.write(link + ";" + str(round(wortluk, 2)).replace(".", ",") + "\n")
            file.close()
        except AttributeError as e:
            pass
        except TypeError as e:
            pass
        except Exception as e:
            print(e)
            pass

    i += 1
