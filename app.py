from flask import Flask, jsonify, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__, static_url_path='/static')

# Database initialization function
def initialize_database():
    con = sqlite3.connect('dbmsproj.db')
    cur = con.cursor()

    # Create tables if not exist
    cur.execute('''CREATE TABLE IF NOT EXISTS manufacturer (
                    man_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT,
                    phno TEXT,
                    country TEXT,
                    state TEXT,
                    city TEXT,
                    pname TEXT UNIQUE,
                    cat TEXT)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS distributor (
                    dist_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT,
                    phno TEXT,
                    cat TEXT,
                    passwd TEXT)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS category (
                    cat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS product (
                    pid INTEGER PRIMARY KEY AUTOINCREMENT,
                    pname TEXT,
                    
                    
                    ppu INTEGER,
                    FOREIGN KEY(pname) REFERENCES manufacturer(pname))''')

    cur.execute('''CREATE TABLE IF NOT EXISTS sales (
                    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    pname TEXT,
                    man TEXT,
                    dist TEXT,
                    total INTEGER,
                    FOREIGN KEY(pname) REFERENCES product(pname),
                    FOREIGN KEY(man) REFERENCES manufacturer(name),
                    FOREIGN KEY(dist) REFERENCES distributor(name))''')

    con.commit()
    con.close()

# Initialize the database
initialize_database()

@app.route('/get_ip')
def get_ip():
    client_ip = request.remote_addr
    return f'The IP address of the client is: {client_ip}'

@app.route('/')
def index():
    return render_template('user.html')

@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        name = request.form['name']

        con = sqlite3.connect('dbmsproj.db')
        cur = con.cursor()
        cur.execute("INSERT INTO category (name) VALUES (?)", (name,))
        con.commit()
        con.close()
        return redirect('/')
    return render_template('category_form.html')

@app.route('/add_distributor', methods=['GET', 'POST'])
def add_distributor():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phno = request.form['phno']
        cat = request.form['cat']
        passwd = request.form['passwd']

        con = sqlite3.connect('dbmsproj.db')
        cur = con.cursor()
        cur.execute("INSERT INTO distributor (name, email, phno, cat, passwd) VALUES (?, ?, ?, ?, ?)",
                    (name, email, phno, cat, passwd))
        con.commit()
        con.close()
        return redirect('/')
    return render_template('distributor_form.html')

@app.route('/add_manufacturer', methods=['GET', 'POST'])
def add_manufacturer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phno = request.form['phno']
        country = request.form['country']
        state = request.form['state']
        city = request.form['city']
        pname = request.form['pname']
        cat = request.form['cat']

        con = sqlite3.connect('dbmsproj.db')
        cur = con.cursor()
        cur.execute("INSERT INTO manufacturer (name, email, phno, country, state, city, pname, cat) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (name, email, phno, country, state, city, pname, cat))
        con.commit()
        con.close()
        return redirect('/')
    
    return render_template('manufacturer_form.html')

@app.route('/view_manufacturers')
def view_manufacturers():
    con = sqlite3.connect('dbmsproj.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM manufacturer")
    manufacturers = cur.fetchall()
    con.close()
    return render_template('view_manufacturers.html', manufacturers=manufacturers)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        pname = request.form['pname']
        
        ppu = request.form['ppu']

        con = sqlite3.connect('dbmsproj.db')
        cur = con.cursor()
        cur.execute("INSERT INTO product (pname, ppu) VALUES (?, ?)",
                    (pname, ppu))
        con.commit()
        con.close()
        return redirect('/')
    return render_template('product_form.html')

@app.route('/add_sales', methods=['GET', 'POST'])
def add_sales():
    if request.method == 'POST':
        date = request.form['date']
        pname = request.form['pname']
        man = request.form['man']
        dist = request.form['dist']
        total = request.form['total']

        con = sqlite3.connect('dbmsproj.db')
        cur = con.cursor()
        cur.execute("INSERT INTO sales (date, pname, man, dist, total) VALUES (?, ?, ?, ?, ?)",
                    (date, pname, man, dist, total))
        con.commit()
        con.close()
        return redirect('/')
    
    # Fetch manufacturers and distributors from the database
    con = sqlite3.connect('dbmsproj.db')
    cur = con.cursor()
    cur.execute("SELECT name FROM manufacturer")
    manufacturers = cur.fetchall()
    cur.execute("SELECT name FROM distributor")
    distributors = cur.fetchall()
    con.close()
    
    return render_template('sales_form.html', manufacturers=manufacturers, distributors=distributors)

# Function to fetch manufacturers from the database
@app.route('/get_manufacturers', methods=['GET'])
def get_manufacturers():
    con = sqlite3.connect('dbmsproj.db')
    cur = con.cursor()
    cur.execute("SELECT name FROM manufacturer")
    manufacturers = cur.fetchall()
    con.close()
    return jsonify({'manufacturers': manufacturers})

# Function to fetch distributors from the database
@app.route('/get_distributors', methods=['GET'])
def get_distributors():
    con = sqlite3.connect('dbmsproj.db')
    cur = con.cursor()
    cur.execute("SELECT name FROM distributor")
    distributors = cur.fetchall()
    con.close()
    return jsonify({'distributors': distributors})

# Function to fetch products from the database
@app.route('/get_products', methods=['GET'])
def get_products():
    con = sqlite3.connect('dbmsproj.db')
    cur = con.cursor()
    cur.execute("SELECT pname FROM product")
    products = cur.fetchall()
    con.close()
    return jsonify({'products': products})

@app.route('/get_ppu', methods=['GET'])
def get_ppu():
    con = sqlite3.connect('dbmsproj.db')
    cur = con.cursor()
    cur.execute("SELECT ppu FROM product")
    ppu = cur.fetchall()
    con.close()
    return jsonify({'ppu': ppu})

    
# Function to fetch categories from the database
@app.route('/get_categories', methods=['GET'])
def get_categories():
    con = sqlite3.connect('dbmsproj.db')
    cur = con.cursor()
    cur.execute("SELECT name FROM category")
    categories = cur.fetchall()
    con.close()
    return jsonify({'categories': categories})



@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')

@app.route('/manufacturer_form.html')
def manufacturer_form():
    return render_template('manufacturer_form.html')

@app.route('/distributor_form.html')
def distributor_form():
    return render_template('distributor_form.html')

@app.route('/product_form.html')
def product_form():
    return render_template('product_form.html')

@app.route('/category_form.html')
def category_form():
    return render_template('category_form.html')

@app.route('/sales_form.html')
def sales_form():
    return render_template('sales_form.html')

if __name__ == '__main__':
    app.run(debug=True)
