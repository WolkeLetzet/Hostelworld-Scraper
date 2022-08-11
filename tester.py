from csv import excel
from pprint import pprint
from time import sleep, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
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
   
   def get_reviews_in_user_page(self,hostel_name):
      reviews_list=self.driver.find_elements(By.CSS_SELECTOR, "div.reviewlisting")
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
            
      return review

            
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
      self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "select-list-slot-wrapper")))
      filtershow= self.driver.find_element(By.CLASS_NAME, "filter.show")
      filtershow.find_element(By.CSS_SELECTOR, "ul > li:last-child").click()
   

#url="https://www.hostelworld.com/pwa/hosteldetails.php/Escarabajo-Hostel/Valparaiso/100905?from=2022-07-27&to=2022-07-30&guests=2&display=reviews"
#url="https://www.hostelworld.com/s?q=Valparaiso,%20Chile&country=Chile&city=Valparaiso&type=city&id=1868&from=2022-07-27&to=2022-07-30&guests=2&HostelNumber=&page=1"
url="https://www.hostelworld.com/pwa/hosteldetails.php/Casa-Volante-Hostal/Valparaiso/82633?from=2022-08-10&to=2022-08-12&guests=2&display=reviews"
driver= WebDriver()

driver.go_to_url_by_class_name(url, "pagination-next")
driver.change_reviews_lang()
driver2= WebDriver()
#print(driver.get_hostel_rate())
review_list=driver.driver.find_elements(By.CSS_SELECTOR, "div.review-item")
reviews=[]
hostel_name=driver.driver.find_element(By.CSS_SELECTOR, "div.title-2").text
continuar=True
while continuar:
   next_page=driver.driver.find_element(By.CSS_SELECTOR, "div.pagination-next")
   
   for item in review_list:
      reviews_num = item.find_element(By.CSS_SELECTOR, "div.user-review > ul > li:last-child").text[0]
      reviews_num = int(reviews_num)
      
      review_date= item.find_element(By.CSS_SELECTOR, "div.review-header > div.date").text
      
      if "2019" in review_date:
         continuar=False
         break
      
      if reviews_num > 1:
         reviewer_url=item.find_element(By.CSS_SELECTOR, "div.user-review > ul > li:last-child > a").get_attribute("href")
         driver2.go_to_url_by_class_name(reviewer_url, "reviewdetails")
         review=driver2.get_reviews_in_user_page(hostel_name)
         reviews.append(review)
         pprint(review)
   
   
   
   if "disabled" in next_page.get_attribute("class"):
      break
   else:
      next_page.click()
print('done\n')
pprint(reviews)
      
      


driver.close()
driver2.close()
