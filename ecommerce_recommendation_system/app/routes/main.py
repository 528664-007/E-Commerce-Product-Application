from flask import Blueprint, render_template, request, redirect, url_for, session
from app.utils.loader import load_products

main_bp = Blueprint('main', __name__)
df = load_products()

# Home Page
@main_bp.route('/')
def home():
    products = df.to_dict(orient='records')
    return render_template('pages/index.html', products=products)

# Product Detail + Recommendations
@main_bp.route('/product/<int:product_id>')
def product(product_id):
    try:
        product = df[df['ProductID'] == product_id].iloc[0].to_dict()
    except IndexError:
        return redirect(url_for('main.home'))

    category = product.get('Category', '')
    recommendations = df[df['Category'] == category].sample(n=4, replace=True).to_dict(orient='records')
    return render_template('pages/product.html', product=product, recommendations=recommendations)

# Search
@main_bp.route('/search')
def search():
    query = request.args.get('query', '').lower()
    filtered = df[df['ProductName'].str.lower().str.contains(query)]
    products = filtered.to_dict(orient='records')
    return render_template('pages/index.html', products=products)

# Login Page
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Dummy login logic – replace with real Firebase/Auth
        username = request.form.get('username')
        if username:
            session['user_name'] = username
        return redirect(url_for('main.home'))
    return render_template('pages/login.html')

# Register Page
@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Dummy registration logic – replace with real Firebase/Auth
        username = request.form.get('username')
        if username:
            session['user_name'] = username
        return redirect(url_for('main.home'))
    return render_template('pages/register.html')

# Logout
@main_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.home'))

# Add to Cart
@main_bp.route('/add-to-cart/<int:product_id>')
def add_to_cart(product_id):
    product_row = df[df['ProductID'] == product_id]
    if not product_row.empty:
        product = product_row.iloc[0].to_dict()
        cart = session.get('cart', [])
        cart.append(product)
        session['cart'] = cart
    return redirect(url_for('main.cart'))

# Cart Page
@main_bp.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = sum([item.get('Price', 0) for item in cart_items])
    return render_template('pages/cart.html', cart=cart_items, total=total)

# Remove from Cart
@main_bp.route('/remove-from-cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    updated_cart = [item for item in cart if item['ProductID'] != product_id]
    session['cart'] = updated_cart
    return redirect(url_for('main.cart'))

# Checkout (Cart Checkout)
@main_bp.route('/checkout')
def checkout():
    cart = session.get('cart', [])
    total = sum([item.get('Price', 0) for item in cart])
    session['cart'] = []  # Clear cart after checkout
    return render_template('pages/checkout.html', cart=cart, total=total)

# ✅ Buy Now (Single Product Checkout)
@main_bp.route('/buy/<int:product_id>')
def buy_now(product_id):
    product_row = df[df['ProductID'] == product_id]
    if not product_row.empty:
        product = product_row.iloc[0].to_dict()
        cart = [product]
        total = product.get('Price', 0)
        return render_template('pages/checkout.html', cart=cart, total=total)
    return redirect(url_for('main.home'))
