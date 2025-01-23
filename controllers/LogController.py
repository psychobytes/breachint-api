from config import db
from datetime import datetime
from models.LogModel import Log, LogRequest

# Fungsi untuk mencatat pencarian ke dalam log
def log_search(search_string):
    log_entry = Log(searchquery=search_string, timestamp=datetime.utcnow())
    db.session.add(log_entry)
    db.session.commit()

# Fungsi untuk mencatat log permintaan
def log_request(method, endpoint, ip_address, user_agent, search_string=None, response_status=200):
    log_entry = LogRequest(
        method=method,
        endpoint=endpoint,
        ip_address=ip_address,
        user_agent=user_agent,
        response_status=response_status,
        timestamp=datetime.utcnow()
    )
    db.session.add(log_entry)
    db.session.commit()

# Fungsi untuk mengambil log pencarian
def get_logs():
    logs = Log.query.all()
    log_list = []
    for log in logs:
        log_list.append({
            'id': log.id,
            'searchquery': log.searchquery,
            'timestamp': log.timestamp.isoformat()
        })

    return log_list
