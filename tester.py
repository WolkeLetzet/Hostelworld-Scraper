from gettext import find
from multiprocessing.connection import wait
from pprint import pprint
from csv import excel
from math import e
from pprint import pprint
from time import time
from warnings import filters
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from soupsieve import select
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep



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
   
   def get_reviews_in_page(self):
      reviews=self.driver.find_elements(By.CSS_SELECTOR, "div.review-item")
      data=[]
      for x in reviews:
         score=float(x.find_element(By.CSS_SELECTOR, "div.score.medium").text)
         date= x.find_element(By.CSS_SELECTOR, "div.date > span").text
         data.append([score,date])
      data=[x for x in data if "2020" in x[1] or "2021" in x[1] or "2022" in x[1]]
      #data.filter(lambda x: "2020" in x[1] or "2021" in x[1] or "2022" in x[1]) # remove reviews from other years
      return data
   
   def close(self):
      self.driver.close()
      self.driver.quit()
   
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
      driver.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "menu")))
      filtershow= self.driver.find_element(By.CLASS_NAME, "filter.show")
      filtershow.find_element(By.CSS_SELECTOR, "ul > li:last-child").click()
   

#url="https://www.hostelworld.com/pwa/hosteldetails.php/Escarabajo-Hostel/Valparaiso/100905?from=2022-07-27&to=2022-07-30&guests=2&display=reviews"
#url="https://www.hostelworld.com/s?q=Valparaiso,%20Chile&country=Chile&city=Valparaiso&type=city&id=1868&from=2022-07-27&to=2022-07-30&guests=2&HostelNumber=&page=1"
url="https://www.hostelworld.com/pwa/hosteldetails.php/Casa-Volante-Hostal/Valparaiso/82633?from=2022-07-28&to=2022-07-30&guests=2&display=reviews"
driver= WebDriver()

driver.go_to_url_by_class_name(url, "pagination-next")
driver.change_reviews_lang()
#print(driver.get_hostel_rate())
reviews=[]

last_page=False
while not last_page:
   reviews_in_page=driver.get_reviews_in_page()
   reviews_in_page=[x for x in reviews_in_page if "2020" in x[1] or "2021" in x[1] or "2022" in x[1]]
   if len(reviews_in_page)==0:
      last_page=True
   else:
      reviews_in_page=[x[0] for x in reviews_in_page]
      reviews.extend(reviews_in_page)
      print(reviews_in_page)
      
   next_page=driver.driver.find_element(By.CSS_SELECTOR, "div.pagination-next")
   
   
   if next_page.get_attribute("class")=="pagination-item pagination-last disabled":
      last_page=True
   else:
      next_page.click()

print(reviews)

driver.close()