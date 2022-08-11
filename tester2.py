from csv import excel
from math import e
from multiprocessing.connection import wait
from pprint import pprint
from time import sleep, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from soupsieve import select
from webdriver_manager.chrome import ChromeDriverManager


class WebDriver():
   
   def __init__(self):
      self.options = Options()
      #self.options.add_argument("--headless")
      self.options.add_argument("--disable-gpu")
      self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
      self.wait = WebDriverWait(self.driver, 10)
   
   def go_to_url_by_class_name(self, url, class_name):
      self.driver.get(url)
      self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, class_name)))  
      
   def go_to_url_by_name(self, url, id):
      self.driver.get(url)
      self.wait.until(EC.presence_of_all_elements_located((By.NAME, id)))
      
   def find_element_by_class_name(self, class_name):
      return self.driver.find_element(By.CLASS_NAME, class_name)
   def find_elements_by_class_name(self, class_name):
      return self.driver.find_elements(By.CLASS_NAME, class_name)
   def find_element_by_id(self, id):
      return self.driver.find_element(By.ID, id)
   def find_element_by_xpath(self, xpath):
      return self.driver.find_element(By.XPATH, xpath)
   def find_elements_by_css_selector(self, css_selector):
      return self.driver.find_elements(By.CSS_SELECTOR, css_selector)       
   def find_element_by_css_selector(self, css_selector):
      return self.driver.find_element(By.CSS_SELECTOR, css_selector)
    
      
   
   def close(self):
      self.driver.close()
      self.driver.quit()
   
   # def get_hostel_rate(self):
   #    section= self.driver.find_element(By.NAME, "reviews-info")
   #    score=section.find_element(By.CSS_SELECTOR, "div.score.big").text
   #    rate= section.find_elements(By.CSS_SELECTOR, "div.rating-score")
   #    rate= [float(x.text) for x in rate]
   #    rate.append(float(score))
   #    return rate
   
   def change_reviews_lang(self):
      filtershow= self.driver.find_element(By.CLASS_NAME, "filter.show")
      filtershow.find_element(By.CLASS_NAME, "select-list-slot-wrapper").click()
      self.driver.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "menu")))
      filtershow= self.driver.find_element(By.CLASS_NAME, "filter.show")
      filtershow.find_element(By.CSS_SELECTOR, "ul > li:last-child").click()
 

hostel_name= "Hostal Po"  
   
driver=WebDriver()
url="https://www.hostelworld.com/profile/4675265/reviews"
driver.go_to_url_by_class_name(url, "reviewdetails")
reviews_list=driver.driver.find_elements(By.CSS_SELECTOR, "div.reviewlisting")
review={'text':[], 'score':[], 'date':[], 'author':[],'author-details':[],'hostel':hostel_name,'rate':[]}
for item in reviews_list:
   hostel_review=item.find_element(By.CSS_SELECTOR, "div.popupreviewlocation >a").text
   if hostel_review==hostel_name:
      review['text']=item.find_element(By.CSS_SELECTOR, "div.reviewtext > p").text
      review['score']=item.find_element(By.CSS_SELECTOR, "div.textrating").text
      review['date']=item.find_element(By.CSS_SELECTOR, "span.reviewdate").text
      review['author']=item.find_element(By.CSS_SELECTOR, "li.reviewername").text
      reviewer_details=item.find_element(By.CSS_SELECTOR, "li.reviewerdetails").text
      reviewer_details=reviewer_details.split(",")
      for field in reviewer_details:
         review['author-details'].append(field.strip())
      
      for index in item.find_elements(By.CSS_SELECTOR, "li.ratinglist > ul > li > span"):
         review["rate"].append(index.text)
      
      

pprint(review)
driver.close()