from csv import excel
from hashlib import new
from operator import ne
from optparse import Values
import openpyxl
from pprint import pprint

class ToExcel:
   def __init__(self, filename):
      self.filename = filename
      self.wb = openpyxl.Workbook()
      self.ws = self.wb.active
      self.ws.append(["Author",
                      "Pais",
                      "Gender",
                      'Edad',
                      'Fecha',
                      "Hostal",
                      'Value For Money',
                      'Security',
                      'Location',
                      'Facilities',
                      'Staff',
                      'Atmosphere',
                      'Cleanliness',
                      "Rate",
                      "Review"])

   def add_review(self, data):
      values= []
      values.append(data['author'])
      values.extend(data['author-details'])
      values.append(data['date'])
      values.append(data['hostel'])
      values.extend(data['rate'])
      values.append(data['score'])
      values.append(data['text'])
      self.ws.append(values)
      
   def save(self):
      self.wb.save(self.filename)
      self.wb.close()
      
# excel_file = ToExcel("hostel_rate.xlsx")


# data ={'author': 'Landon',
#  'author-details': ['Canada', 'Male', '31-40'],
#  'date': '19th Feb 2020',
#  'hostel': 'La Nona B&B',
#  'rate': ['10.0', '10.0', '10.0', '10.0', '10.0', '10.0', '10.0'],
#  'score': '10.0',
#  'text': "La Nona offers superlative hospitality, the best I've ever "
#          'experienced in all my years of travelling. After five nights in '
#          'Valpo, I felt more like family than a guest. Rene is a tremendous '
#          'host, with no shortage of suggestions for what to do in the city and '
#          'elsewhere in Chile. The facilities were all excellent and very '
#          'clean. My room was lovely, with a small courtyard right outside the '
#          'door. Breakfast is simply superb. I already feel homesick, and am '
#          'planning my next visit to La Nona in my mind.'}

# values= []
# values.append(data['author'])
# values.extend(data['author-details'])
# values.append(data['date'])
# values.append(data['hostel'])
# values.extend(data['rate'])
# values.append(data['score'])
# values.append(data['text'])
# pprint(values)
# excel_file.ws.append(values)

# excel_file.save()