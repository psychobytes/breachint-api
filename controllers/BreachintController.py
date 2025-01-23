from flask import jsonify, request
from flask_jwt_extended import jwt_required

from config import db_mongo
from config import collection
from config import collection2


from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required
from controllers.LogController import log_search, get_logs  # Import fungsi dari LogController

from config import db 

app = Flask(__name__)

# @jwt_required()
def search():
    data = request.get_json()
    searchquery = data.get('searchquery')

    # Mencatat log setiap kali ada pencarian
    log_search(searchquery)  
    
    # dukcapilresult = dukcapil(searchquery)
    dukcapilresult = dukcapil(searchquery)
    mypertaminaresult = mypertamina(searchquery)

    return jsonify({'result': dukcapilresult,
                    'result2': mypertaminaresult})

def dukcapil(search_string):
    # Menggunakan pencarian teks
    query = {
        "$text": {
            "$search": f'"{search_string}"'
        }
    }
    results = collection.find(query)  # Mengambil dokumen yang sesuai

    output = []
    for result in results:
        # Mengonversi ObjectId ke string sebelum mengembalikannya
        result['_id'] = str(result['_id'])  # Pastikan _id dikonversi ke string
        output.append(result)
        
    if not output:
        return "Data tidak ditemukan."

    return output

def mypertamina(search_string):
    # Menggunakan pencarian teks
    query = {
        "$text": {
            "$search": f'"{search_string}"'
        }
    }
    results = collection2.find(query)  # Mengambil dokumen yang sesuai

    output = []
    for result in results:
        # Mengonversi ObjectId ke string sebelum mengembalikannya
        result['_id'] = str(result['_id'])  # Pastikan _id dikonversi ke string
        output.append(result)
    
    if not output:
        return "Data tidak ditemukan."

    return output

# Route untuk menampilkan log pencarian
@app.route('/logs', methods=['GET'])
@jwt_required()  # Hanya bisa diakses oleh user yang terautentikasi
def get_log_entries():
    logs = get_logs()  # Memanggil fungsi get_logs dari LogController

    return jsonify({'logs': logs})

if __name__ == '__main__':
    app.run(debug=True)
