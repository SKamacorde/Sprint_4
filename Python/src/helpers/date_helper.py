from datetime import datetime
import pandas as pd

class DateHelper:
    @staticmethod
    def now():
        """Retorna data e hora atual."""
        return datetime.now()
    
    def parse_date(date_str):
            try:
               return datetime.strptime(date_str, "%d/%m/%y %H:%M:%S")
            except Exception:
                return pd.NaT
            
    def parse_datetime_auto(data_str):    
        for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
            try:
                return datetime.strptime(data_str, fmt)
            except ValueError:
                continue
            raise ValueError(f"Formato de data inválido: {data_str}")