import openpyxl

class ToExcel:
   def __init__(self, filename,options:list[bool]=[True,True,True,True]):
      self.filename = filename
      self.wb = openpyxl.Workbook()
      self.ws = self.wb.active
      self.header=["Author", "Pais","Gender",'Edad','Fecha',"Hostal","Score"]
                     
      if options[0]:
         self.header.extend(['Value For Money','Security','Location','Facilities','Staff','Atmosphere','Cleanliness'])
      if options[2]:
         self.header.append('Comentario')
      
      self.ws.append(self.header)
      
   def add_review(self, data,options:list[bool]=[True,True,True,True]):
      values= []
      values.append(data['author'])
      values.extend(data['author-details'])
      values.append(data['date'])
      values.append(data['hostel'])
      values.append(data['score'])
      if options[0]:
         values.extend(data['rate'])
      if options[2]:
         values.append(data['text'])
      self.ws.append(values)
      
   def save(self):
      self.wb.save(self.filename)
      self.wb.close()
      
