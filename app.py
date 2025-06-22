from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Dummy products database
PRODUCTS = {
    1: {'id': 1, 'name': 'Watch', 'price': 49.99},
    2: {'id': 2, 'name': 'Headphones', 'price': 29.99},
    3: {'id': 3, 'name': 'Laptop Stand', 'price': 19.99},
}

@app.route('/')
def index():
    return render_template('index.html', products=PRODUCTS)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['admin'] = True
            return redirect(url_for('admin_panel'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/admin')
def admin_panel():
    if not session.get('admin'):
        return redirect(url_for('login'))
    return render_template('admin.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# --------------------- CART ROUTES ------------------------

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, qty in cart.items():
        product = PRODUCTS.get(int(product_id))
        if product:
            subtotal = qty * product['price']
            cart_items.append({**product, 'qty': qty, 'subtotal': subtotal})
            total += subtotal
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    cart.pop(str(product_id), None)
    session['cart'] = cart
    return redirect(url_for('view_cart'))

if __name__ == '__main__':
    app.run(debug=True)
