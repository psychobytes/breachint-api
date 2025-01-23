from config import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

# Definisikan model untuk tabel 'log' di MySQL
class Log(db.Model):
    __tablename__ = 'log_search'  
    id = Column(Integer, primary_key=True)  
    searchquery = Column(String(255), nullable=False)  
    timestamp = Column(DateTime, default=datetime.utcnow) 

    def __repr__(self):
        return f"<Log(id={self.id}, searchquery={self.searchquery}, timestamp={self.timestamp})>"

# Definisikan model untuk tabel 'log_request' di MySQL
class LogRequest(db.Model):
    __tablename__ = 'log_request'
    id = Column(Integer, primary_key=True)
    method = Column(String(10), nullable=False)  
    endpoint = Column(String(255), nullable=False) 
    ip_address = Column(String(45), nullable=False)  
    user_agent = Column(String(255), nullable=False)   
    response_status = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow) 

    def __repr__(self):
        return (f"<LogRequest(id={self.id}, method={self.method}, endpoint={self.endpoint}, "
                f"ip_address={self.ip_address}, user_agent={self.user_agent}, "
                f"search_query={self.search_query}, response_status={self.response_status}, "
                f"timestamp={self.timestamp})>")