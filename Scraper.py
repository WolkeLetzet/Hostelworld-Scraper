from bs4 import BeautifulSoup
import requests
from to_csv import to_csv

class Scraper():
   
   def __init__(self) -> None:
      self.reviews=[]
      self.counter =0
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
                           'rango_edad': rev['groupInformation']['age'],
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


from pprint import pprint
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class SeleniumScraper():
   def __init__(self):
      self.options = Options()
      self.options.add_argument("--headless")
      self.options.add_argument("--disable-gpu")
      self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
      self.wait = WebDriverWait(self.driver,15)
      
   def go_to_url_by_class_name(self, url:str,class_name:str):
      self.driver.get(url)
      self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, class_name)))
   
   def go_to_url_by_css_selector(self, url:str,css_selector:str):
      self.driver.get(url)
      self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector)))
   
   def go_to_url_by_name(self, url:str,name:str):
      self.driver.get(url)
      self.wait.until(EC.presence_of_all_elements_located((By.NAME, name)))
      
   def find_elements_by_css(self,css_selector:str):
      return self.driver.find_elements(By.CSS_SELECTOR, css_selector)
   
   def find_elements_by_class_name(self,class_name:str):
      return self.driver.find_elements(By.CLASS_NAME,class_name)
   
   def find_elements_by_name(self,name:str):
      return self.driver.find_elements(By.NAME,name)
   
   def find_elements_by_ID(self,id:str):
      return self.driver.find_elements(By.ID,id)
   
   def find_element_by_css(self,css_selector:str):
      return self.driver.find_element(By.CSS_SELECTOR, css_selector)
   
   def find_element_by_class_name(self,class_name:str):
      return self.driver.find_element(By.CLASS_NAME,class_name)
   
   def find_element_by_name(self,name:str):
      return self.driver.find_element(By.NAME,name)
   
   def find_element_by_ID(self,id:str):
      return self.driver.find_element(By.ID,id)
   
   def wait_until_presAll_css_selector(self,css_selector):
      self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,css_selector)))
      
   def wait_until_presAll_class_name(self,class_name):
      self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,class_name)))
   
   def close(self):
      """Cierra el driver"""
      self.driver.close()
      self.driver.quit()
   
   def get_hostels_url(self):
      
      """Obtiene una lista con los url hacia la pagina de comentarios de todos los Hostales que aparecen""" 
      urls=[]
      cont=True
      while cont:
         #lista de objetos elementos "a" dentro de tag "div" con clase bottom-rating 
         review_url = self.find_elements_by_css("div.property > div.info > div.bottom-rating > a")
         
         
         #filtra y extrae el atributo "href" de todos los elementos todos los hostales que se puedan visitar
         aux = [x.get_attribute('href') for x in review_url if x.get_attribute("href")]
         pprint(aux) 
         urls.extend(aux)
         if self.hasPaginationOrNext():
            builder = ActionChains(self.driver)
            a =self.find_element_by_css("div.pagination-next")

            # builder.move_to_element(a).click().perform()
            # #a.click()
            
            self.driver.execute_script("arguments[0].click();",a)
            
         else:
            break

            
      return urls
   
   def change_reviews_lang(self):
      """Cambia la preferencia del idioma del filtro de comentarios"""
      
      filtershow= self.find_element_by_class_name("filter.show")
      filtershow.find_element(By.CLASS_NAME, "select-list-slot-wrapper").click()
      self.wait_until_presAll_class_name("menu")
      filtershow= self.find_element_by_class_name("filter.show")
      filtershow.find_element(By.CSS_SELECTOR, "ul > li:last-child").click()
      
   def hasPaginationOrNext(self):
      try: 
         pagination = self.find_element_by_css('div.pagination.pagination')
         nxt = pagination.find_element(By.CSS_SELECTOR,'div.pagination-next').get_attribute('class')
         pprint(nxt)
         if 'disabled' in nxt:
            return False
         else:
            return True
      except:
         return False
            
   def get_reviews_in_user_page(self,hostel_name:str):
      
      """
      Obtiene  una lista de puntajes del hostal buscado en la pagina del usuario
      ----
      hostel_name : String
         nombre del hostal cuya reseña se busca
      
      """
      #obtener todas las reviews del usuario
      reviews_list=self.find_elements_by_css("div.reviewlisting")
      
      for item in reviews_list: 
         hostel_review=item.find_element(By.CSS_SELECTOR, "div.popupreviewlocation >a").text 
         if hostel_review==hostel_name:
            rating_list = item.find_elements(By.CSS_SELECTOR,"ul > li.ratinglist > ul > li > span")
            return [x.text for x in rating_list]
   
   
def formatter(lista:list):
   lista[7]= lista[7].replace('\n','')
   lista[7]= lista[7].replace('\r','')
   lista[7]= lista[7].replace('\t','')

   dic = {
         "nombre_hostel":lista[0],
         "nombre_reseñador":lista[1],
         "rango_edad":lista[2],
         "grupo":lista[3],
         "valor_dinero":lista[4][0],
         "seguridad":lista[4][1],
         "localizacion":lista[4][2],
         "facilidades":lista[4][3],
         "personal":lista[4][4],
         "atmosfera":lista[4][5],
         "limpieza":lista[4][6],
         "general":lista[5],
         "fecha":lista[6],
         "comentario":lista[7]         
      }
   return dic
   
def seleniumMainloop(filename:str,url:str):
      driver1 = SeleniumScraper()
      driver2 = SeleniumScraper()
      saver = to_csv(filename=filename)
      
      ###### LINKS  DE  LOS  HOSTELS  ########
      driver1.go_to_url_by_css_selector(url,'div.property-card > div.property')
      
      hostel_link= driver1.get_hostels_url()
      ##############################################
      
      
      
      for link in hostel_link:
         
         driver1.go_to_url_by_class_name(link,'pagination')
         driver1.change_reviews_lang()
         
         try:
            hostel_name = driver1.find_element_by_css("div > div:nth-child(2) > section > div:nth-child(4) > div > div:nth-child(1) > h1 > div").text
         except:
            hostel_name= None
            
         #lista de elementos reviews 
         review_list=driver1.driver.find_elements(By.CSS_SELECTOR, "div.review-item")
         reviews_num=1
         for item in review_list:
            
            try:
               reviews_num = item.find_element(By.CSS_SELECTOR, "div.user-review > ul > li:last-child").text[0]
               reviews_num = int(reviews_num)
         
            except: 
               continue
            
            
            reviewer_name= item.find_element(By.CSS_SELECTOR,"div.user-review.user-review > ul > li.name.body-2").text
            
            rango_edad=  item.find_element(By.CSS_SELECTOR,"div.user-review.user-review > ul > li.details.body-3").text.split(",")[1].replace(" ","")
            
            grupo = item.find_element(By.CSS_SELECTOR,"div.user-review.user-review > ul > li.details.body-3").text.split(",")[0].replace(" ","")
            
            review = [hostel_name,reviewer_name,rango_edad,grupo]
            
            if reviews_num >1 :
               try:
                  reviwer_link=item.find_element(By.CSS_SELECTOR,"div.user-review.user-review > ul > li.total-reviews.body-3 > a").get_attribute("href")
                  driver2.go_to_url_by_class_name(reviwer_link,"reviewdetails")
                  rate= driver2.get_reviews_in_user_page(hostel_name)
               except:
                  rate = [0,0,0,0,0,0,0]
                  continue
               
            else:
               rate = [0,0,0,0,0,0,0]
            
            review.append(rate)
               
            try:
               comentario = item.find_element(By.CSS_SELECTOR,"div.review-content > div.review-notes.body-2").text
            except:
               comentario = None
            
            try :
               puntaje_general = item.find_element(By.CSS_SELECTOR,"div.review-content > div.review-header > div.rating > div > div.score.medium").text
            except:
               puntaje_general = None
               
            try :
               fecha = item.find_element(By.CSS_SELECTOR,"div.review-content > div.review-header > div.date.body-3 > span").text
            except:
               fecha = None
               
            review.extend([
                  puntaje_general,
                  fecha,
                  comentario
               ])
            pprint(review)
            saver.saveData([formatter(review)])
            