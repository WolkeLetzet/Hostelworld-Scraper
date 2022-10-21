from tkinter import mainloop
from bs4 import BeautifulSoup
import requests
from to_csv import to_csv


class Scraper():

    def __init__(self, options=[True, True, True, True]) -> None:
        self.reviews = []
        self.counter = 0
        self.options = options
        self.properties = None

    def getPropertiesIDs(self, city: str) -> list:
        propiertyType: str = 'hostels'
        ids = []
        url = "https://www.hostelworld.com/%s/%s/" % (
            propiertyType, city.replace(' ', '-'))
        req = requests.get(url)

        while True:

            soup = BeautifulSoup(req.text, features="lxml")
            last = soup.select(
                'ul.pagination > li.arrow-last > a')[0].get('href')
            nxt = soup.select(
                'ul.pagination > li.arrow.pagination-next > a')[0].get('href')
            print(req.url)
            elements = soup.find_all('div', 'fabresult')
            ids.extend([x['data-id'] for x in elements])

            if last == req.url:
                break
            req = requests.get(nxt)

        return ids

    def getPropiertyDetails(self, propertyId):
        if type(propertyId) == str:

            url = "https://api.m.hostelworld.com/2.2/properties/%s" % propertyId
            print(url)
            return requests.get(url).json()

        elif hasattr(propertyId, '__iter__'):
            properties = []
            for i in propertyId:
                url = "https://api.m.hostelworld.com/2.2/properties/%s" % i
                print(url)
                properties.append(requests.get(url).json())
            return properties

    def getPropertyReviews(self, propertyId: str):
        ''' Obtiene las reviews de un hostel por su Id'''
        url = "https://api.m.hostelworld.com/2.2/properties/%s/reviews/" % propertyId
        url += "?allLanguages=true"

        revs = {'reviews': []}

        while True:
            print(url)
            try:
                req = requests.get(url).json()
                # pprint(req)
                nxt = req['pagination']['next']
                revs['reviews'].extend(req['reviews'])
            except:
                return revs

            if nxt == None:
                break
            else:
                url = 'https://api.m.hostelworld.com/2.2'+nxt+"&allLanguages=true"
        return revs

    def formatter(self, propertyReviews, propertyDetails):
        reviews = []

        for rev in propertyReviews['reviews']:
            if rev['user']['gender'] is None:
                rev['user']['gender'] = {'id': None}

            text = rev['notes'].replace('\n', '')
            text = text.replace('\r', '')
            text = text.replace('\t', '')

            reviews.append({'reseña_id': rev['id'],
                            'lenguaje': rev['languageCode'],
                            'fecha': rev['date'].replace('-', '/'),
                            'id_reseñador': rev['user']['id'],
                            'genero': rev['user']['gender']['id'],
                            'nacionalidad': rev['user']['nationality']['name'],
                            'apodo': rev['user']['nickname'],
                            'id_propiedad': propertyDetails['id'],
                            'nombre_propiedad': propertyDetails['name'],
                            'valor_dinero': rev['rating']['value'],
                            'seguridad': rev['rating']['safety'],
                            'locacion': rev['rating']['location'],
                            'personal': rev['rating']['staff'],
                            'atmosfera': rev['rating']['atmosphere'],
                            'limpieza': rev['rating']['cleanliness'],
                            'facilidades': rev['rating']['facilities'],
                            'general': rev['rating']['overall'],
                            'texto': text
                            })

        # self.reviews.extend(reviews)
        return reviews

    def getCounter(self):
        return self.counter

    def setPropertiesIDs(self, city):
        self.properties = self.getPropertiesIDs(city)

    def mainloop(self, filename, city):

        if not self.properties:
            self.properties = self.getPropertiesIDs(city)

        saver = to_csv(filename)
        for id in self.properties:
            try:
                details = self.getPropiertyDetails(id)
                reviews = self.getPropertyReviews(id)
                reviews = self.formatter(
                    propertyReviews=reviews, propertyDetails=details)
                self.counter += 1
            except:
                pass
            finally:

                saver.saveData(reviews)
        self.counter = 0
        self.properties = None

# scrap = Scraper()
# scrap.mainloop('la-serena.csv','la-serena')
