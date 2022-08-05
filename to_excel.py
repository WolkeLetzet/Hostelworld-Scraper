from csv import excel
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
      
