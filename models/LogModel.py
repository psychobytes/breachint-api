from config import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

# Definisikan model untuk tabel 'log' di MySQL
class Log(db.Model):
    __tablename__ = 'log_search'  # Nama tabel di MySQL
    id = Column(Integer, primary_key=True)  # ID sebagai primary key
    searchquery = Column(String(255), nullable=False)  # Kolom untuk query pencarian
    timestamp = Column(DateTime, default=datetime.utcnow)  # Waktu pencarian

    def __repr__(self):
        return f"<Log(id={self.id}, searchquery={self.searchquery}, timestamp={self.timestamp})>"