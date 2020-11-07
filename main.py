import requests
from bs4 import BeautifulSoup


url="https://www.epey.com/akilli-telefonlar/e/Tjtfczo5OiJwdWFuOkRFU0MiOw==/"
headers = { 
    'Accept': '*/*',
    'Host': 'www.epey.com',      
    'Connection': 'keep-alive', 
    'X-Requested-With':'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.317'
    }
    
    
s = requests.Session()

i=1
while i<92:
    r = s.get(url+str(i),headers=headers, timeout=None)
    print( 'get: ', r.status_code,"i: ",i)
    soup = BeautifulSoup(r.text, 'html.parser')

    containers= soup.find_all("ul",class_="metin row")

    for tel in containers:
        try:
            link = tel.find("li",class_="fiyat cell").a.get("href")
            fiyat =tel.find("li",class_="fiyat cell").a.text.split()[0].replace(".","").split(",")[0] #tl
            puan = tel.find("li",class_="puan cell").div["data-text"]

            wortluk= int (fiyat)/int(puan)
            file=open("ekmekler1.csv","a", encoding="utf8")
            file.write(link+";"+str( round(wortluk,2)).replace(".",",")+"\n")
            file.close() 
        except Exception as e:
            print(e)
            pass
    i+=1


