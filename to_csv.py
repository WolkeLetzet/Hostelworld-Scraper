import csv
from os.path import exists


class to_csv:

    def __init__(self, filename: str) -> None:

        self.filename = filename

    def loadData(self):

        with open(self.filename, 'r', newline='', encoding='utf-8') as fp:
            reader = csv.DictReader(fp, fieldnames=self.header, delimiter=';')
            self.data = [row for row in reader]

    def saveData(self, data:list[dict], stream=None):
        '''Guardar lista de diccionarios en un documento CSV'''
        self.header=data[0].keys()
        need_header = not exists(self.filename) and not bool(stream)
        with stream or open(self.filename, 'a', newline='', encoding='utf-8-sig') as fp:
            writer = csv.DictWriter(fp, fieldnames=list(data[0].keys()), delimiter=';')
            try:
                if need_header:
                    writer.writeheader()
                if isinstance(data, list):
                    writer.writerows(data)
                else:
                    writer.writerow(data)
            finally:
                pass
