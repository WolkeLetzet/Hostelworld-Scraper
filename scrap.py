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

   def change_reviews_lang(self):
      filtershow= self.driver.find_element(By.CLASS_NAME, "filter.show")
      filtershow.find_element(By.CLASS_NAME, "select-list-slot-wrapper").click()
      self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "menu")))
      filtershow= self.driver.find_element(By.CLASS_NAME, "filter.show")
      filtershow.find_element(By.CSS_SELECTOR, "ul > li:last-child").click()

   def get_reviews_in_user_page(self,hostel_name,options=[True,True,True]):
      reviews_list=self.driver.find_elements(By.CSS_SELECTOR, "div.reviewlisting")
      
      reviews=[]
      for item in reviews_list:
         hostel_review=item.find_element(By.CSS_SELECTOR, "div.popupreviewlocation >a").text
         if hostel_review==hostel_name:
            review={'text':[], 'score':[], 'date':[], 'author':[],'author-details':[],'hostel':hostel_name,'rate':[]}
            
            if options[2] :
               review['text']=item.find_element(By.CSS_SELECTOR, "div.reviewtext").text
            
            if options[0]:
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

def main(url="",excel_name="reviews.xlsx",options=[True,True,True,True]):

   driver= HostelScraper()
   links=driver.get_hostel_coments_url(url)
   pprint(links)
   driver2= HostelScraper()
   excel_book=ToExcel(excel_name)

   for link in links:
      driver.go_to_url_by_class_name(link, "pagination-next")
      if options[0]:
         try:
            driver.change_reviews_lang()
         except:
            pass
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
               reviews=driver2.get_reviews_in_user_page(hostel_name,options)
               
               try:
                  for rev in reviews:
                     
                     excel_book.add_review(rev)
                     excel_book.wb.save(excel_name)
               except:
                  pass
            elif reviews_num == 1 and options[3]:
               review={'text':[], 'score':[], 'date':[], 'author':[],'author-details':[],'hostel':hostel_name,'rate':[0,0,0,0,0,0,0]}
               review['author']=item.find_element(By.CSS_SELECTOR,"li.name").text
               review["author-details"].append('Null')
               
               reviewer_details=item.find_element(By.CSS_SELECTOR,"li.details").text
               reviewer_details=reviewer_details.split(",")
               
               for field in reviewer_details:
                  review['author-details'].append(field.strip())
               
               review["text"]=item.find_element(By.CSS_SELECTOR,"div.review-notes").text
               review['score']=item.find_element(By.CSS_SELECTOR,"div.score").text
               review['date']=item.find_element(By.CSS_SELECTOR,"div.date > span").text
               
               try:
                  excel_book.add_review(review)
                  excel_book.wb.save(excel_name)
               except:
                  pass
               
               
         if "disabled" in next_page.get_attribute("class"):
            break
         else:
            try:
               next_page.click()
            except:
               break
            
   excel_book.save()

   driver.close()
   driver2.close()

