from flask import jsonify, request
from flask_jwt_extended import jwt_required

from config import db_mongo
from config import collection
from config import collection2

from controllers.LogController import log_request, log_search, get_logs
from flask import Flask

app = Flask(__name__)

@jwt_required()
def search():
    data = request.get_json()
    searchquery = data.get('searchquery')

    # Ambil informasi dari permintaan
    user_agent = request.headers.get('User-Agent', 'Unknown User-Agent') 
    ip_address = request.remote_addr
    method = request.method
    endpoint = request.path

    # Log permintaan
    log_request(method, endpoint, ip_address, user_agent) 
    log_search(searchquery)  
    
    dukcapilresult = dukcapil(searchquery)
    mypertaminaresult = mypertamina(searchquery)

    response_status = 200 

    return jsonify({'dukcapil': dukcapilresult,
                    'mypertamina': mypertaminaresult}), response_status


def dukcapil(search_string):
    query = {
        "$text": {
            "$search": f'"{search_string}"'
        }
    }
    results = collection.find(query) 

    output = []
    for result in results:
        result['_id'] = str(result['_id']) 
        output.append(result)      
    if not output:
        res = {"Error":"Data tidak ditemukan."}
        output.append(res)

    return output


def mypertamina(search_string):
    query = {
        "$text": {
            "$search": f'"{search_string}"'
        }
    }
    results = collection2.find(query)  

    output = []
    for result in results:
        result['_id'] = str(result['_id'])  
        output.append(result)
    
    if not output:
        res = {"Error":"Data tidak ditemukan."}
        output.append(res)

    return output

# Route untuk menampilkan log pencarian
@jwt_required()  
def get_log_entries():
    logs = get_logs()  

    return jsonify({'logs': logs})

# Menambahkan error handler global di aplikasi Flask
@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"An error occurred: {str(e)}")
    return jsonify({"message": "An internal error occurred. Please try again later."}), 500

@app.errorhandler(OSError)
def handle_os_error(e):
    app.logger.error(f"OS error occurred: {str(e)}")
    return jsonify({"message": "An operating system error occurred. Please check your configuration."}), 500

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except OSError as e:
        if e.errno == 10038:
            print("Error: An operation was attempted on something that is not a socket.")
        else:
            print(f"An unexpected OS error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
