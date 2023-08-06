import pandas as pd
import sqlalchemy
from unidecode import unidecode

server_list = {
    'innovacion': '10.111.145.180\\sqlinnovacion',
    'gestion_clinica': '10.111.145.180\\sqlclinica',
    'convenio': '10.111.145.180\\sqlconvenio',
    'patcore': '10.111.145.180\\sqlclinica',
    'bioslis': '10.111.145.180\\sqlclinica',
    'mosaiq': '10.111.145.180\\sqlclinica',
    'contraloria': '10.111.145.180\\sqlconvenio'
}

db_list = {
    'innovacion': 'Innova',
    'gestion_clinica': 'Gestion_Clin',
    'patcore': 'PatCore',
    'bioslis': 'BiosLIS-FALP',
    'mosaiq': 'MOSAIQ',
    'contraloria': 'Gestion_Contraloria',
    'convenio': 'Gestion_Convenio'
}

class Conn:
    def __init__(self, base, usr, pwd):
        self.base = unidecode(base.lower())
        self.usr = usr
        self.pwd = pwd

    def db_query(self, query):
        self.query = query

        if self.base in server_list and self.base in db_list:
            conn_string = f"mssql+pymssql://{self.usr}:{self.pwd}@{server_list[self.base]}/{db_list[self.base]}?charset=utf8"
            engine = sqlalchemy.create_engine(conn_string)
            conn = engine.connect()
            result = conn.execute(sqlalchemy.text(query))
            df = pd.DataFrame(result.fetchall(), columns=[i for i in result.keys()])
            return df
        else:
            return "No se puede conectar a la base de datos"
