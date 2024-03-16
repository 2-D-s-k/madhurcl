from flask import Flask, render_template, request, g
import sqlite3

app = Flask(__name__)

DATABASE = 'product_database.db'

# Create or connect to the SQLite database
conn = sqlite3.connect('product_database.db')
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL,
                    stock_quantity INTEGER,
                    category TEXT,
                    manufacture_date TEXT,
                    vendor_name TEXT
                )''')
conn.commit()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    cursor = get_db().cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    return render_template('index.html', products=products)

@app.route('/add_product', methods=['POST'])
def add_product():
    cursor = get_db().cursor()
    name = request.form['name']
    description = request.form['description']
    price = float(request.form['price'])
    stock_quantity = int(request.form['stock_quantity'])
    category = request.form['category']
    manufacture_date = request.form['manufacture_date']
    vendor_name = request.form['vendor_name']

    cursor.execute('''INSERT INTO products (name, description, price, stock_quantity, category, manufacture_date, vendor_name)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (name, description, price, stock_quantity, category, manufacture_date, vendor_name))
    get_db().commit()
    return index()

if __name__ == '__main__':
    app.run(debug=True)
