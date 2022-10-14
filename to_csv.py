import csv
from os.path import exists

class to_csv :
   
   def __init__(self,filename:str) -> None:
      self.header = ['reseña_id','lenguaje','fecha',
          'reseñador_id','genero','nacionalidad','apodo',
          'propiedad_id','nombre_propiedad',
          'valor_dinero','seguridad','locacion','personal','atmosfera','limpieza','facilidades','general',
          'texto'
          ]
      self.filename= filename
   
   def loadData(self):
      
      with open(self.filename,'r',newline='',encoding='utf-8') as fp: 
         reader = csv.DictReader(fp,fieldnames=self.header,delimiter=';')
         self.data=[row for row in reader]
   
   def saveData(self,data):
      
         if not exists(self.filename): 
            a=True
         with open(self.filename,'a',newline='',encoding='utf-8') as fp:
            writer= csv.DictWriter(fp,fieldnames=self.header,delimiter=';')
            try:
               if a:
                  writer.writeheader()
            except:
               pass
            finally:   
               if type(data) == list:
                  writer.writerows(data)
               else:
                  writer.writerow(data)