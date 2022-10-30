from bs4 import BeautifulSoup
import requests
from to_csv import to_csv

class Scraper():
   
   def __init__(self,options=[True,True,True,True]) -> None:
      self.reviews=[]
      self.counter =0
      self.options = options
      self.properties = None
      self.exception = None
   
   def getPropertiesIDs(self,continent:str,country:str,city:str) -> list:
      propiertyType:str='hostels'
      ids=[]
      url="https://www.hostelworld.com/st/%s/%s/%s/%s" %(propiertyType,continent,country,city.replace(' ','-'))
      req= requests.get(url)
      errUrl = "https://www.hostelworld.com/st/%s/%s/%s/" %(propiertyType,continent,country)
      errReq= requests.get(errUrl)
      print('\n'+req.url)
      print(errReq.url+'\n')
      
      if req.url == errReq.url:
         raise Exception('No se Encontro la ciudad')
      while True:
         #variables efimeras del ciclo
         soup = BeautifulSoup(req.text,features="lxml")
         
         try:
            next_last = soup.select('div.pagination > div.arrow-last > a')[0].get('href')
            next_nxt  = soup.select('div.pagination > div.arrow.pagination-next > a')[0].get('href')
         except IndexError:
            next_last = req.url
            next_nxt = req.url
            
         print(req.url)
         elements = soup.select('div.property > div.details-col > div > h2 > a')
         retrieved_ids = [x.get('href').split('/')[6] for x in elements]
         ids.extend(retrieved_ids)
         
         if next_last == req.url:
            break
         else:
            req = requests.get(next_nxt)

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
                           'genero': rev['user']['gender']['id'],
                           'agrupación': rev['groupInformation']['groupTypeCode'],
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
   
   
   def setPropertiesIDs(self,continent,country,city):
      self.properties= self.getPropertiesIDs(continent,country,city)
      
   def getEx(self):
      return self.exception
   
   def mainloop(self,filename:str,continent,country,city):

      try:
         self.properties = self.getPropertiesIDs(continent,country,city)
      except Exception as ex:
         self.exception = ex
         
         
      saver = to_csv(filename)
      
      csvStream = None
      
      for iD in self.properties :
         try: 
            details = self.getPropiertyDetails(iD)
            sreviews = self.getPropertyReviews(iD)
            
            reviews = self.formatter(propertyReviews=sreviews,propertyDetails=details)
            self.counter+=1
         except Exception as e:
            pass
         finally:
            if len(reviews) > 0:
               saver.saveData(reviews, csvStream)
               
      self.counter = 0
      self.properties = None      

#main('la-serena.csv','la-serena')
   