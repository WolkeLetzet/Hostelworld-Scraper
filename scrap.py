from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from to_excel import ToExcel


class HostelScraper:
   def __init__(self):
      self.options = Options()
      self.options.add_argument("--headless")
      self.options.add_argument("--disable-gpu")
      self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
      self.wait = WebDriverWait(self.driver, 10)
        
   def get_hostel_coments_url(self, url:str):
      
      """Obtiene una lista con los url hacia la pagina de comentarios de todos los Hostales que aparecen"""
      
      self.go_to_url_by_class_name(url, "info") # abre el url y espera a que aparescan todos los elementos con clase "info"
      review_url = self.driver.find_elements(By.CSS_SELECTOR, "div.bottom-rating > a") #lista de objetos elementos "a" dentro de tag "div" con clase bottom-rating 
      urls= [x for x in review_url if x.get_attribute("href")] #filtra todos los hostales que se puedan visitar
      urls= [x.get_attribute("href") for x in urls] #extrae el atributo "href" de todos los elementos
      return urls
   
######### Metodos GO TO #######
#abren una pagina por url y espera hasta que aparezcan los elementos definidos en los parametros
   def go_to_url_by_class_name(self, url,class_name):
      self.driver.get(url)
      self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, class_name)))
   
   def go_to_url_by_css_selector(self, url,css_selector):
      self.driver.get(url)
      self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, css_selector)))
   
   def go_to_url_by_name(self, url,name):
      self.driver.get(url)
      self.wait.until(EC.presence_of_all_elements_located((By.NAME, name)))
         

   def change_reviews_lang(self):
      """Cambia la preferencia del idioma del filtro de comentarios"""
      
      filtershow= self.driver.find_element(By.CLASS_NAME, "filter.show")
      filtershow.find_element(By.CLASS_NAME, "select-list-slot-wrapper").click()
      self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "menu")))
      filtershow= self.driver.find_element(By.CLASS_NAME, "filter.show")
      filtershow.find_element(By.CSS_SELECTOR, "ul > li:last-child").click()

   def get_reviews_in_user_page(self,hostel_name:str,options=[True,True,True]):
      
      """
      Obtiene  una lista de reseña del hostal buscado en la pagina del usuario
      ----
      hostel_name : String
         nombre del hostal cuya reseña se busca
      
      """
      
      reviews_list=self.driver.find_elements(By.CSS_SELECTOR, "div.reviewlisting") #obtiene todas las reviews del usuario
      
      reviews=[] #lista de reviews
      for item in reviews_list: 
         hostel_review=item.find_element(By.CSS_SELECTOR, "div.popupreviewlocation >a").text #obtiene el nombre del hostal en la review
         if hostel_review==hostel_name: #si el nombre del hostal de la review es igual al buscado
            review={'text':[], 'score':[], 'date':[], 'author':[],'author-details':[],'hostel':hostel_name,'rate':[]} #instancia una review
            
            if options[2] : #si estan habilitados los comentarios
               review['text']=item.find_element(By.CSS_SELECTOR, "div.reviewtext").text #obtiene el comentario de la review
            
            
            review['score']=item.find_element(By.CSS_SELECTOR, "div.textrating").text #obtiene el puntaje del review
            
            review['date']=item.find_element(By.CSS_SELECTOR, "span.reviewdate").text #obtiene la fecha de la review
            review['author']=item.find_element(By.CSS_SELECTOR, "li.reviewername").text #obtiene el nombre del autor
            reviewer_details=item.find_element(By.CSS_SELECTOR, "li.reviewerdetails").text #obtiene los detalles del usuario
            
            #cambia el formato de los detalles del autor
            reviewer_details=reviewer_details.split(",")
            for field in reviewer_details:
               review['author-details'].append(field.strip())
               
            if options[0]: #si los valores estan habilitados
               
               for index in item.find_elements(By.CSS_SELECTOR, "li.ratinglist > ul > li > span"): #obtiene los valores de la review
                  review["rate"].append(index.text)
            else:
               review["rate"]=['0','0','0','0','0','0','0']
            
            reviews.append(review) #agrega la review a la lista
            
      return reviews
   


   
   def close(self):
      """Cierra el driver"""
      self.driver.close()
      self.driver.quit()

def main(url:str,excel_name:str="reviews.xlsx",options:list[bool]=[True,True,True,True]):

   driver= HostelScraper() #iniciar driver
   
   links=driver.get_hostel_coments_url(url) #obtener los links hacia los comentarios de todos los hostales
   
   pprint(links)
   driver2= HostelScraper() #iniciar driver secundario
   excel_book=ToExcel(excel_name,options) #crear objeto ToExcel

   for link in links: #por cada enlace
      #el driver principal se dirige a la seccion de comentarios del hostel y espera hasta que cargue el elemento de clase "pagination-next"
      driver.go_to_url_by_class_name(link, "pagination-next")
      
      if options[1]: # si esta habilitado el cambio de lenguaje de las reviews
         try:
            driver.change_reviews_lang()  #cambio de lenguaje de las reviews
         except:
            pass
         
      review_list=driver.driver.find_elements(By.CSS_SELECTOR, "div.review-item") #lista de elementos reviews 
      reviews=[]
      hostel_name=driver.driver.find_element(By.CSS_SELECTOR, "div.title-2").text #nombre del hostal
      continuar=True
      
      while continuar:
         next_page=driver.driver.find_element(By.CSS_SELECTOR, "div.pagination-next") #elemento "next-page"
         
         for item in review_list: #por cada review
            #cantidad de reviews del reviewer
            try:
               reviews_num = item.find_element(By.CSS_SELECTOR, "div.user-review > ul > li:last-child").text[0]
               reviews_num = int(reviews_num)
            
            except: 
               continue
            
            review_date= item.find_element(By.CSS_SELECTOR, "div.review-header > div.date").text #fecha de la review
            
            # #detener al llegar al año 
            # if "2019" in review_date: 
            #    continuar=False
            #    break
            
            if reviews_num > 1: #si la cantidad de reviews es mayor a uno
               reviewer_url=item.find_element(By.CSS_SELECTOR, "div.user-review > ul > li:last-child > a").get_attribute("href") #url hacia las reviews del reviwer
               driver2.go_to_url_by_class_name(reviewer_url, "reviewdetails") #el driver secundario se dirige hacia las reviews del reviwer
               reviews=driver2.get_reviews_in_user_page(hostel_name,options)
               
               try:
                  for rev in reviews:
                     print("\n")
                     pprint(rev)
                     print("\n")
                     excel_book.add_review(rev,options)
                     excel_book.save()
               except:
                  pass
            elif reviews_num == 1 and options[3]: 
               review={'text':[], 'score':[], 'date':[], 'author':[],'author-details':[],'hostel':hostel_name,'rate':[]}
               review['author']=item.find_element(By.CSS_SELECTOR,"li.name").text
               review["author-details"].append('Null') #pais null
               
               reviewer_details=item.find_element(By.CSS_SELECTOR,"li.details").text
               reviewer_details=reviewer_details.split(",")
               
               for field in reviewer_details:
                  review['author-details'].append(field.strip())
               
               review["text"]=item.find_element(By.CSS_SELECTOR,"div.review-notes").text
               review['score']=item.find_element(By.CSS_SELECTOR,"div.score").text
               review['date']=item.find_element(By.CSS_SELECTOR,"div.date > span").text
               
               if options[0]:
                  review["rate"]=['0','0','0','0','0','0','0']
               try:
                  print("\n")
                  pprint(review)
                  print("\n")
                  excel_book.add_review(review,options)
                  excel_book.save()
               except:
                  pass
               
               
         if "disabled" in next_page.get_attribute("class"):
            break
         else:
            try:
               next_page.click() #pagina siguiente
            except:
               break
            
   excel_book.save() #guardar libro

   driver.close() #cerrar driver
   driver2.close() #driver