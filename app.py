from flask import Flask, render_template, redirect, url_for, request, session
import csv

app = Flask(__name__)
app.secret_key = 'tajny_klucz'

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with open('users.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[0] == username and row[1] == password:
                    session['username'] = username
                    return redirect(url_for('profile'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        localisation = request.form['localisation']
        with open('users.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([username, password,localisation])
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    if request.method == 'POST':
        with open('profiles.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([username, request.form['about_me']])
    return render_template('profile.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    results = []
    with open('profiles.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if query.lower() in row[1].lower():
                results.append(row[0])
    return render_template('search.html', results=results)
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
