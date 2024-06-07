class Item:
    def __init__(self):
        self.data = {
            "link": "",
            "wortluk": "",
            "fiyat": "",
        }

    def get_data(self):
        return self.data

    def set_link(self, link):
        self.data["link"] = link

    def set_wortluk(self, wortluk):
        self.data["wortluk"] = wortluk

    def set_fiyat(self, fiyat):
        self.data["fiyat"] = fiyat
