from flask import render_template
from webstore import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/product-list')
def product_list():
    return render_template('product-list.html')


@app.route('/product-detail')
def product_detail():
    return render_template('product-detail.html')


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
