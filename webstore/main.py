from flask import render_template
from webstore import app
from webstore.models import Product



@app.route('/')
def index():
    products = Product.query.filter(Product.id.startswith("SS")).all()
    return render_template('index.html', products= products)


@app.route('/product-list')
def product_list():
    products = Product.query.filter(Product.category_id.startswith("1")).all()
    return render_template('product-list.html', products=products)


@app.route('/product-detail')
def product_detail():
    products = Product.query.filter(Product.category_id.startswith("1")).all()
    return render_template('product-detail.html', products=products)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/checkout')
def checkout():
    return render_template('checkout.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/my-account')
def my_account():
    return render_template('my-account.html')


@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000)
