import pymssql
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

class BaseRepository:
    def __init__(self):
        self.server = os.getenv('DB_SERVER')       # ex: '192.168.0.120'
        self.database = os.getenv('DB_NAME')       # ex: 'Fiap_Agro'
        self.user = os.getenv('DB_USER')           # ex: 'sa'
        self.password = os.getenv('DB_PASSWORD')   # ex: 'L11e5@01'
        self.port = int(os.getenv('DB_PORT', 1433))  # padrão SQL Server 1433

    def get_connection(self):
        try:
            conn = pymssql.connect(
                server=self.server,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            return conn
        except pymssql.Error as e:
            print("❌ Erro ao conectar ao SQL Server:")
            print(e)
            return None
