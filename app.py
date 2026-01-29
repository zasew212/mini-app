from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.permanent_session_lifetime = timedelta(days=1)

# Admin credentials
ADMIN_USERNAME = "osamo_444"
ADMIN_PASSWORD = "kovalev311010"  # Change this in production

# Sample data for products
products = [
    {
        "id": 1,
        "name": "Nike Air Force 1",
        "category": "обувь",
        "size": "42",
        "condition": "Новое",
        "price": "12,000 ₽",
        "description": "Оригинальные Nike Air Force 1, белый цвет, размер 42. Состояние новое, в коробке.",
        "images": ["https://via.placeholder.com/300x200?text=Nike+AF1", "https://via.placeholder.com/300x200?text=Nike+AF1+Side"]
    },
    {
        "id": 2,
        "name": "Adidas Hoodie",
        "category": "одежда",
        "size": "L",
        "condition": "БУ",
        "price": "4,500 ₽",
        "description": "Черный худи Adidas, размер L. Состояние отличное, почти как новое.",
        "images": ["https://via.placeholder.com/300x200?text=Adidas+Hoodie", "https://via.placeholder.com/300x200?text=Adidas+Back"]
    },
    {
        "id": 3,
        "name": "Apple Watch Series 7",
        "category": "другое",
        "size": "Универсальный",
        "condition": "Новое",
        "price": "25,000 ₽",
        "description": "Apple Watch Series 7, 45mm, серебристый цвет. Полностью функционален.",
        "images": ["https://via.placeholder.com/300x200?text=Apple+Watch", "https://via.placeholder.com/300x200?text=Watch+Side"]
    }
]

@app.route('/')
def home():
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return render_template('product_detail.html', product=product)
    return redirect(url_for('home'))

@app.route('/admin')
def admin_login():
    return render_template('admin_login.html')

@app.route('/admin/login', methods=['POST'])
def admin_auth():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['admin_logged_in'] = True
        session.permanent = True
        return redirect(url_for('admin_panel'))
    return redirect(url_for('admin_login'))

@app.route('/admin/panel')
def admin_panel():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('admin_panel.html', products=products)

@app.route('/admin/add_product', methods=['GET', 'POST'])
def add_product():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        images = []
        for i in range(1, 6):
            image_url = request.form.get(f'image{i}')
            if image_url:
                images.append(image_url)

        new_product = {
            "id": len(products) + 1,
            "name": request.form.get('name'),
            "category": request.form.get('category'),
            "size": request.form.get('size'),
            "condition": request.form.get('condition'),
            "price": request.form.get('price'),
            "description": request.form.get('description'),
            "images": images if images else ["https://via.placeholder.com/300x200?text=No+Image"]
        }
        products.append(new_product)
        return redirect(url_for('admin_panel'))

    return render_template('add_product.html')

@app.route('/admin/delete_product/<int:product_id>')
def delete_product(product_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    global products
    products = [p for p in products if p['id'] != product_id]
    return redirect(url_for('admin_panel'))

@app.route('/admin/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return redirect(url_for('admin_panel'))

    if request.method == 'POST':
        # Update basic product info
        product['name'] = request.form.get('name')
        product['category'] = request.form.get('category')
        product['size'] = request.form.get('size')
        product['condition'] = request.form.get('condition')
        product['price'] = request.form.get('price')
        product['description'] = request.form.get('description')

        # Update images - collect all 5 image URLs
        images = []
        for i in range(1, 6):
            image_url = request.form.get(f'image{i}')
            if image_url:  # Only add non-empty image URLs
                images.append(image_url)

        # Ensure at least one image
        product['images'] = images if images else ["https://via.placeholder.com/300x200?text=No+Image"]

        return redirect(url_for('admin_panel'))

    return render_template('edit_product.html', product=product)

@app.route('/filter_products', methods=['POST'])
def filter_products():
    data = request.get_json()
    category = data.get('category', '')
    size = data.get('size', '')
    condition = data.get('condition', '')

    filtered_products = products

    if category:
        filtered_products = [p for p in filtered_products if p['category'] == category]
    if size:
        filtered_products = [p for p in filtered_products if p['size'] == size]
    if condition:
        filtered_products = [p for p in filtered_products if p['condition'] == condition]

    return jsonify({'products': filtered_products})

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
