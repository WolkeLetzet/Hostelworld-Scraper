from gettext import find
from multiprocessing.connection import wait
from pprint import pprint
from csv import excel
from math import e
from pprint import pprint
from time import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
   
   def get_hostel_rate(self):      
      
      rating = self.driver.find_elements(By.CLASS_NAME, "rating-score") # get all ratings
      rating.extend(self.driver.find_elements(By.CSS_SELECTOR, "div.score.orange.big")) # get the big orange score
      rating= [x.text for x in rating] # if x.text]
      rating= [x for x in rating if x] # remove empty strings
      rating= [float(x) for x in rating]# convert to float
      return rating # return a list of ratings
   
   def get_hostel_users_score(self):
      score= self.driver.find_elements(By.CSS_SELECTOR, "div.score.orange.medium")
      score= [x.text for x in score] # if x.text]
      score= [x for x in score if x] # remove empty strings
      score= [float(x) for x in score]# convert to float
      return score
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

#url= "https://www.hostelworld.com/pwa/hosteldetails.php/Casa-Volante-Hostal/Valparaiso/82633?from=2022-07-26&to=2022-07-29&guests=2&display=reviews"
url="https://www.hostelworld.com/pwa/hosteldetails.php/Escarabajo-Hostel/Valparaiso/100905?from=2022-07-26&to=2022-07-29&guests=2&display=reviews"
driver= WebDriver()
driver.go_to_url_by_class_name(url, "pagination")
date= driver.find_elements_by_css_selector("div.date>span")
date= [x.text for x in date if "2022" in x.text or "2021" in x.text or "2020" in x.text]

      
print(date)

driver.close()