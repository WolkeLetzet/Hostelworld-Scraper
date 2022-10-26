import csv
from os.path import exists


class to_csv:

    def __init__(self, filename: str) -> None:
        self.header = ['id_reseña', 'lenguaje', 'fecha',
                       'id_reseñador', 'agrupación','genero','edad', 'nacionalidad', 'apodo',
                       'id_propiedad', 'nombre_propiedad',
                       'valor_por_dinero', 'seguridad', 'ubicacion', 'personal', 'atmosfera', 'limpieza', 'facilidades', 'puntaje_general',
                       'comentario_turista'
                       ]
        self.filename = filename

    def loadData(self):

        with open(self.filename, 'r', newline='', encoding='utf-8') as fp:
            reader = csv.DictReader(fp, fieldnames=self.header, delimiter=';')
            self.data = [row for row in reader]

    def saveData(self, data, stream=None):
        need_header = not exists(self.filename) and not bool(stream)
        with stream or open(self.filename, 'a', newline='', encoding='utf-8') as fp:
            writer = csv.DictWriter(fp, fieldnames=self.header, delimiter=';')
            try:
                if need_header:
                    writer.writeheader()
                if isinstance(data, list):
                    writer.writerows(data)
                else:
                    writer.writerow(data)
            finally:
                pass
