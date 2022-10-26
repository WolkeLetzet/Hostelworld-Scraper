from io import StringIO
import pandas as pd
from bs4 import BeautifulSoup
import requests
from to_csv import to_csv

class Scraper():
   
   def __init__(self,options=[True,True,True,True]) -> None:
      self.reviews=[]
      self.counter =0
      self.options = options
      self.properties = None
   
   def getPropertiesIDs(self,city:str) -> list:
      propiertyType:str='hostels'
      ids=[]
      url="https://www.hostelworld.com/%s/%s/" %(propiertyType,city.replace(' ','-'))
      req= requests.get(url)
      attempts = 4  # intentos por request
      last, nxt = None, None
      while True:
         #variables efimeras del ciclo
         next_last, next_nxt, retrieved_ids = None, None, None
         for attempt in range(attempts):
            try:
               soup = BeautifulSoup(req.text,features="lxml")
               next_last = soup.select('ul.pagination > li.arrow-last > a')[0].get('href')
               next_nxt  = soup.select('ul.pagination > li.arrow.pagination-next > a')[0].get('href')
               print(req.url)
               elements = soup.find_all('div','fabresult')
               retrieved_ids = [x['data-id'] for x in elements]
               break
            except IndexError:
               print(f'Attempt: {attempt + 1}')
         if not all((e is not None) for e in (next_last, next_nxt, retrieved_ids)):
            raise Exception('Max attempts reached') # falla por maximos intentos
         last, nxt = next_last, next_nxt # guardar las variables efimeras del ciclo para el ciclo siguiente
         ids.extend(retrieved_ids)
         if last == req.url:
            break
         req = requests.get(nxt)

      return ids
   
   def getPropiertyDetails(self,propertyId):
      if type(propertyId) == str:
         
         url="https://api.m.hostelworld.com/2.2/properties/%s" %propertyId
         print(url)
         return requests.get(url).json()
         
      elif hasattr(propertyId,'__iter__'):
         properties=[]
         for i in propertyId:
            url="https://api.m.hostelworld.com/2.2/properties/%s" %i
            print(url)
            properties.append(requests.get(url).json())
         return properties
      
   def getPropertyReviews(self,propertyId:str):
      
      ''' Obtiene las reviews de un hostel por su Id'''
      url="https://api.m.hostelworld.com/2.2/properties/%s/reviews/" %propertyId
      url+= "?allLanguages=true"
      
      revs= {'reviews':[]}
      
      while True:
         print(url)
         try :
            req = requests.get(url).json()
            #pprint(req)
            nxt = req['pagination']['next']
            revs['reviews'].extend(req['reviews'])
         except:
            return revs
         
         if nxt == None :
            break
         else:
            url = 'https://api.m.hostelworld.com/2.2'+nxt+"&allLanguages=true"
      return revs
   
   def formatter(self,propertyReviews,propertyDetails):
      reviews=[]
      
      for rev in propertyReviews['reviews']:
         if rev['user']['gender'] is None:
            rev['user']['gender'] = {'id':None}
            
         text= rev['notes'].replace('\n','')
         text=text.replace('\r','')
         text=text.replace('\t','')

         reviews.append({  'id_reseña':rev['id'],
                           'lenguaje':rev['languageCode'],
                           'fecha':rev['date'].replace('-','/'),
                           'id_reseñador':rev['user']['id'],
                           'genero': rev['user']['gender'],
                           'agrupación': rev['groupInformation']['groupTypeCode']['id'],
                           'edad': rev['groupInformation']['age'],
                           'nacionalidad': rev['user']['nationality']['name'],
                           'apodo':rev['user']['nickname'],
                           'id_propiedad':propertyDetails['id'],
                           'nombre_propiedad':propertyDetails['name'],
                           'valor_por_dinero':rev['rating']['value'],
                           'seguridad':rev['rating']['safety'],
                           'ubicacion':rev['rating']['location'],
                           'personal':rev['rating']['staff'],
                           'atmosfera':rev['rating']['atmosphere'],
                           'limpieza':rev['rating']['cleanliness'],
                           'facilidades':rev['rating']['facilities'],
                           'puntaje_general':rev['rating']['overall'],
                           'comentario_turista': text
                        })
         
      #self.reviews.extend(reviews)
      return reviews
   
   def getCounter(self):
      return self.counter
   
   def setPropertiesIDs(self,city):
      self.properties= self.getPropertiesIDs(city)
   
   def mainloop(self,filename:str,city):
      
      if not self.properties:
         self.properties = self.getPropertiesIDs(city)
         
      saver = to_csv(filename)
      
      csvStream = None
      if filename.endswith('.xlsx'):
         csvStream = StringIO('')
         csvStream.close = lambda: None
      
      for id in self.properties :
         try: 
            details = self.getPropiertyDetails(id)
            reviews = self.getPropertyReviews(id)
            reviews = self.formatter(propertyReviews=reviews,propertyDetails=details)
            self.counter+=1
         except:
            pass
         finally:
            saver.saveData(reviews, csvStream)
      if bool(csvStream):
         csvStream.seek(0) # Lo hace leible desde la primera linea del archivo de a mentiritas
         pd.read_csv(csvStream, sep=";", header='infer', names=saver.header).to_excel(filename, index=None, header=True)
      self.counter = 0
      self.properties = None      

#main('la-serena.csv','la-serena')
   