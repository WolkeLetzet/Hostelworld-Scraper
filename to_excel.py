from csv import excel
from hashlib import new
from operator import ne
import openpyxl

class ToExcel:
   def __init__(self, filename):
      self.filename = filename
      self.wb = openpyxl.Workbook()
      self.ws = self.wb.active
      self.ws.title = 'Puntajes de Usuarios'
      self.ws2 = self.wb.create_sheet(title='Ascpectos')
      self.ws2.append(['Seguridad', 'Localización', 'Staff', 'Atmosfera', 'Limpieza', 'Facilidades', 'Valoración'])
      self.ws.append(('Puntaje',))

   def add_row_at_sheet1(self, row):
      self.ws.append(row)
      
   def add_row_at_sheet2(self, row):
      self.ws2.append(row)
      
   def save(self):
      self.wb.save(self.filename)
      self.wb.close()
      
excel_file = ToExcel("hostel_rate.xlsx")
