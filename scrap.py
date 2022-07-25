from pprint import pprint
import webdriver_manager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

url = "https://www.hostelworld.com/s?q=Valparaiso,%20Chile&country=Chile&city=Valparaiso&type=city&id=1868&from=2022-07-25&to=2022-07-28&guests=2&HostelNumber=&page=1"

class HostelScraper:
   def __init__(self):
      self.options = Options()
      #self.options.add_argument("--headless")
      self.options.add_argument("--disable-gpu")
      self.driver = webdriver.Chrome(executable_path= r"C:\Users\n1_na\Downloads\chromedriver_win32\chromedriver.exe", options=self.options)
      self.wait = WebDriverWait(self.driver, 10)
      
      
   def get_hostel_rate_url(self, url):
      self.driver.get(url)
      self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "info")))
      review_url = self.driver.find_elements(By.CSS_SELECTOR, "div.bottom-rating > a")
      urls= [x for x in review_url if x.get_attribute("href")]
      urls= [x.get_attribute("href") for x in urls]
      return urls
   
   def get_hostel_rate(self, url):
      self.driver.get(url)
      self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.score.orange.medium")))
      
      rating = self.driver.find_elements(By.CLASS_NAME, "rating-score")
      rating= [x.text for x in rating]
      rating= [x for x in rating if x]
      
      rate = self.driver.find_elements(By.CSS_SELECTOR, "div.score")
      rate= [x.text for x in rate]
      rate= [x for x in rate if x] 
      return rate,rating


scraper= HostelScraper()
urls=scraper.get_hostel_rate_url(url)


a=[]
for url in urls:
   a.append(scraper.get_hostel_rate(url))
   pprint(a)
   print("\n")

