from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from to_excel import ToExcel

url = "https://www.hostelworld.com/s?q=Valparaiso,%20Chile&country=Chile&city=Valparaiso&type=city&id=1868&from=2022-07-25&to=2022-07-28&guests=2&HostelNumber=&page=1"

class HostelScraper:
   def __init__(self):
      self.options = Options()
      #self.options.add_argument("--headless")
      self.options.add_argument("--disable-gpu")
      self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
      self.wait = WebDriverWait(self.driver, 10)
      
   
   def get_hostel_coments_url(self, url,limit=1):
      self.go_to_url_by_class_name(url, "info")
      review_url = self.driver.find_elements(By.CSS_SELECTOR, "div.bottom-rating > a")
      urls= [x for x in review_url if x.get_attribute("href")]
      urls= [x.get_attribute("href") for x in urls]
      return urls
   
   def go_to_url_by_class_name(self, url,class_name):
      self.driver.get(url)
      self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, class_name)))
   
   def go_to_url_by_css_selector(self, url,css_selector):
      self.driver.get(url)
      self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, css_selector)))
   
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
   
   def close(self):
      self.driver.close()
      self.driver.quit()

driver= HostelScraper()
urls=driver.get_hostel_coments_url(url)
pprint(urls)

for url in urls:

   driver.go_to_url_by_class_name(url, "pagination-next")
   next_page= driver.driver.find_element(By.CLASS_NAME, "pagination-next")
   score= driver.get_hostel_users_score()
   rate= driver.get_hostel_rate()
   pprint(rate)
   while next_page.get_dom_attribute("class") != "pagination-item pagination-next disabled":
      next_page.click()
      score.extend(driver.get_hostel_users_score())
      next_page = driver.driver.find_element(By.CLASS_NAME, "pagination-next")
      
   pprint(score)
   print("\n")



driver.close()

