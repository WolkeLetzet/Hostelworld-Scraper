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
   def go_to_url_by_name(self, url,name):
      self.driver.get(url)
      self.wait.until(EC.presence_of_all_elements_located((By.NAME, name)))
         
   def get_hostel_rate(self):
      section= self.driver.find_element(By.NAME, "reviews-info")
      score=section.find_element(By.CSS_SELECTOR, "div.score.big").text
      rate= section.find_elements(By.CSS_SELECTOR, "div.rating-score")
      rate= [float(x.text) for x in rate]
      rate.append(float(score))
      return rate

   def get_reviews_in_page(self):
      reviews=self.driver.find_elements(By.CSS_SELECTOR, "div.review.review-item")
      data=[]
      #data=[x[0] for x in data if "2020" in x[1] or "2021" in x[1] or "2022" in x[1]]# remove old reviews
      #data.filter(lambda x: "2020" in x[1] or "2021" in x[1] or "2022" in x[1]) # remove reviews from other years
      return data
   
   def change_reviews_lang(self):
      filtershow= self.driver.find_element(By.CLASS_NAME, "filter.show")
      filtershow.find_element(By.CLASS_NAME, "select-list-slot-wrapper").click()
      self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "menu")))
      filtershow= self.driver.find_element(By.CLASS_NAME, "filter.show")
      filtershow.find_element(By.CSS_SELECTOR, "ul > li:last-child").click()
   
   def close(self):
      self.driver.close()
      self.driver.quit()

url = "https://www.hostelworld.com/s?q=Valparaiso,%20Chile&country=Chile&city=Valparaiso&type=city&id=1868&from=2022-07-30&to=2022-08-02&guests=2&HostelNumber=&page=1"

driver= HostelScraper()
links=driver.get_hostel_coments_url(url)
pprint(links)
reviews=[]

for link in links:
   driver.go_to_url_by_class_name(link, "pagination-next")
   driver.change_reviews_lang()
   last_page=False
   hostel_reviews=[]
   rate=driver.get_hostel_rate()
   
   while not last_page: # get all reviews in page
      reviews_in_page=driver.get_reviews_in_page()
      reviews_in_page=[x for x in reviews_in_page if "2020" in x[1] or "2021" in x[1] or "2022" in x[1]]# remove old reviews
      
      next_page=driver.driver.find_element(By.CSS_SELECTOR, "div.pagination-item.pagination-next")
      
      if not reviews_in_page:
         break # if there are no reviews in page, then it is the last page
      else:
         reviews_in_page=[x[0] for x in reviews_in_page]
         hostel_reviews.extend(reviews_in_page)
         print(reviews_in_page)
      
      if next_page.get_attribute("class")=="pagination-item pagination-next disabled": # if it is the last page
         break
      else:
         next_page.click()
   reviews.append([rate,hostel_reviews])
print(reviews)
driver.close()

