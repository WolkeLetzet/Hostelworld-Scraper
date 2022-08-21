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
        
   def get_hostels_url(self, url,limit=1):
      """obitene una lista de urls de hostales en la pagina de la url dada"""
      self.go_to_url_by_class_name(url, "info")
      review_url = self.driver.find_elements(By.CSS_SELECTOR, "div.bottom-rating > a")
      urls= [x for x in review_url if x.get_attribute("href")]
      urls= [x.get_attribute("href") for x in urls]
      return urls
   
   def go_to_url_by_class_name(self, url,class_name):
      """se dirige a la pagina dada y espera a que se cargue el elemento con el nombre de clase dado"""
      self.driver.get(url)
      self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, class_name)))
   
   def go_to_url_by_css_selector(self, url,css_selector):
      """se dirige a la pagina dada y espera a que se cargue el elemento con el selector CSS dado"""
      self.driver.get(url)
      self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, css_selector)))
   
   def go_to_url_by_name(self, url,name):
      """se dirige a la pagina dada y espera a que se cargue el elemento con el atributo 'name' dado"""
      self.driver.get(url)
      self.wait.until(EC.presence_of_all_elements_located((By.NAME, name)))
         
   def get_hostel_rate(self):
      section= self.driver.find_element(By.NAME, "reviews-info")
      score=section.find_element(By.CSS_SELECTOR, "div.score.big").text
      rate= section.find_elements(By.CSS_SELECTOR, "div.rating-score")
      rate= [float(x.text) for x in rate]
      rate.append(float(score))
      return rate

   def change_reviews_lang(self):
      filtershow= self.driver.find_element(By.CLASS_NAME, "filter.show")
      filtershow.find_element(By.CLASS_NAME, "select-list-slot-wrapper").click()
      self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "menu")))
      filtershow= self.driver.find_element(By.CLASS_NAME, "filter.show")
      filtershow.find_element(By.CSS_SELECTOR, "ul > li:last-child").click()

   def get_reviews_in_user_page(self,hostel_name):
      reviews_list=self.driver.find_elements(By.CSS_SELECTOR, "div.reviewlisting")
      
      reviews=[]
      for item in reviews_list:
         hostel_review=item.find_element(By.CSS_SELECTOR, "div.popupreviewlocation >a").text
         if hostel_review==hostel_name:
            review={'text':[], 'score':[], 'date':[], 'author':[],'author-details':[],'hostel':hostel_name,'rate':[]}
            review['text']=item.find_element(By.CSS_SELECTOR, "div.reviewtext").text
            review['score']=item.find_element(By.CSS_SELECTOR, "div.textrating").text
            review['date']=item.find_element(By.CSS_SELECTOR, "span.reviewdate").text
            review['author']=item.find_element(By.CSS_SELECTOR, "li.reviewername").text
            reviewer_details=item.find_element(By.CSS_SELECTOR, "li.reviewerdetails").text
            reviewer_details=reviewer_details.split(",")
            for field in reviewer_details:
               review['author-details'].append(field.strip())
            
            for index in item.find_elements(By.CSS_SELECTOR, "li.ratinglist > ul > li > span"):
               review["rate"].append(index.text)
            
            reviews.append(review)
            
      return reviews
   
   def close(self):
      self.driver.close()
      self.driver.quit()

class ThreadScraper:
   
   def __init__(self,url):
      self.url=url
      self.hostel_scraper=HostelScraper()
      self.to_excel=ToExcel()
      
   def get_hostels_url(self):
      return self.hostel_scraper.get_hostels_url(self.url) 
   
   
   

def main(url,options=None):
   global ventana1, current_review
   ventana1=HostelScraper()
   
   

   