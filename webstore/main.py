from flask import render_template, request, redirect, session, url_for
from webstore import app, utils, login
from webstore.models import Product
from flask_login import logout_user, login_user
from webstore.models import *


@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


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



@app.route("/login", methods=["get", "post"])
def login():
    err_msg = ""
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user = utils.check_login(username=username, password=password)
        if user:
            login_user(user=user)
            if "next" in request.args:
                return redirect(request.args["next"])

            return redirect(url_for('index'))
        else:
            err_msg = "Something wrong!!!"

    return render_template("login.html", err_msg=err_msg)


@app.route("/logout")
def logout():
    logout_user()

    return redirect(url_for("index"))


@app.route("/register", methods=["get", "post"])
def register():
    if session.get("user"):
        return redirect(request.url)

    err_msg = ""
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if password.strip() != confirm.strip():
            err_msg = "Mat khau khong khop"
        else:
            if utils.add_user(name=name, username=username, password=password):
                return redirect(url_for("login"))
            else:
                err_msg = "Something Wrong!!!"

    return render_template("register.html", err_msg=err_msg)




if __name__ == '__main__':
    app.run(debug=True, port=8000)
