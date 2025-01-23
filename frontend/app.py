from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import jsonify
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Ganti dengan kunci rahasia Anda

#admin
@app.route('/admin/login')
def home():
    return render_template('login.html')

@app.route('/admin/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Kirim permintaan ke API untuk login
    response = requests.post('http://127.0.0.1:5000/admin/login', json={
        'username': username,
        'password': password
    })

    if response.status_code == 200:
        data = response.json()
        access_token = data.get('access_token')
        # Simpan token di session atau lakukan tindakan lain
        # Misalnya, menyimpan token di session
        session['access_token'] = access_token
        flash('Login successful! Token: ' + access_token)
        return redirect(url_for('admin'))  # Redirect ke halaman lain setelah login
    else:
        flash('Login failed: ' + response.json().get('msg', 'Unknown error'))
        return redirect(url_for('home'))

@app.route('/admin')
def admin():
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('home'))

    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('http://127.0.0.1:5000/admin/users',headers=headers)
    usersdata = response.json()
    users=usersdata['data']['user']
    return render_template('admin.html', users=users)

@app.route('/admin', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')  # Tangkap email
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({'message': 'Missing fields'}), 400

    headers = {'Authorization': f"Bearer {session['access_token']}"}
    response = requests.post('http://127.0.0.1:5000/admin/users', json=data, headers=headers)
    return response.text, response.status_code

@app.route('/admin/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not all([username, email, password]):
        return jsonify({'message': 'Missing fields'}), 400  # Pastikan semua field ada

    headers = {'Authorization': f"Bearer {session['access_token']}"}
    response = requests.put(f'http://127.0.0.1:5000/admin/users/{user_id}', json=data, headers=headers)
    return response.text, response.status_code

@app.route('/admin/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    headers = {'Authorization': f"Bearer {session['access_token']}"}
    response = requests.delete(f'http://127.0.0.1:5000/admin/users/{user_id}', headers=headers)
    return response.text, response.status_code

@app.route('/admin/logout', methods=['GET'])
def admin_logout():
    # Hapus token dari session
    session.pop('access_token', None)
    return redirect(url_for('home'))  

#user
#user menage
@app.route('/user/login')
def user_home():
    return render_template('user-login.html')

@app.route('/user/login', methods=['POST'])
def user_login():
    email = request.form.get('email')
    password = request.form.get('password')
    response = requests.post('http://127.0.0.1:5000/user/login', json={
        'email': email,
        'password': password
    })
    if response.status_code == 200:
        data = response.json()
        access_token = data.get('access_token')
        session['access_token'] = access_token
        flash('Login successful! Token: ' + access_token)
        return redirect(url_for('breachdata'))
    else:
        flash('Login failed: ' + response.json().get('message', 'Unknown error'))
        return redirect(url_for('user_home'))

@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email') 
        password = data.get('password')
        if not all([username, email, password]):
            return jsonify({'message': 'Missing fields'}), 400
        response = requests.post('http://127.0.0.1:5000/user/register', json=data)
        return response.text, response.status_code
    else:
        return render_template('user-register.html')

@app.route('/')
def breachdata():
    access_token = session.get('access_token')
    if not access_token:
        flash('You need to log in to access this page.')
        return redirect(url_for('user_home'))
    return render_template('index.html')

@app.route('/', methods=['POST'])
def search():
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('/user/login'))

    searchquery = request.form.get('searchquery')

    # send request to search
    response = requests.post('http://127.0.0.1:5000/api/search', json={
        'searchquery': searchquery
    })

    result = response.text

    results = json.loads(result)

    result = results.get('result')
    result2 = results.get('result2')

    return render_template('index.html', result = result, result2 = result2)


@app.route('/logout', methods=['GET'])
def user_logout():
    session.pop('access_token', None)
    return redirect(url_for('user_home'))

if __name__ == '__main__':
    app.run(port=5001, debug=True)