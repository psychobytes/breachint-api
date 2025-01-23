from config import db
from datetime import datetime
from models.LogModel import Log

# Fungsi untuk mencatat pencarian ke dalam log
def log_search(search_string):
    log_entry = Log(searchquery=search_string, timestamp=datetime.utcnow())
    
    # Menyimpan log ke dalam tabel log di MySQL
    db.session.add(log_entry)
    db.session.commit()

# Fungsi untuk mengambil log pencarian
def get_logs():
    # Mengambil seluruh log dari tabel log
    logs = Log.query.all()

    # Mengonversi hasilnya ke list dan mengubah objek menjadi dictionary
    log_list = []
    for log in logs:
        log_list.append({
            'id': log.id,
            'searchquery': log.searchquery,
            'timestamp': log.timestamp.isoformat()  # Mengonversi timestamp menjadi string ISO
        })

    return log_list
