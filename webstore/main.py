from flask import render_template, request, redirect, session, url_for
from flask_login import logout_user, login_user, login_required
from flask_mail import Message, Mail
from sqlalchemy.exc import IntegrityError
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from webstore import app, utils, login, mail
from webstore.models import *


randomToken = URLSafeTimedSerializer('this_is_a_secret_key')


@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/product-list')
def product_list():
    products = Product.query.filter(Product.category_id.startswith("1")).all()
    return render_template('product-list.html', products=products)


@app.route('/product-detail')
def product_detail():
    products = Product.query.filter(Product.category_id.startswith("1")).all()
    return render_template('product-detail.html', products=products)


@app.route('/cart')
@login_required
def cart():
    return render_template('cart.html')


@app.route('/checkout')
@login_required
def checkout():
    return render_template('checkout.html')


@app.route('/contact')
@login_required
def contact():
    return render_template('contact.html')


@app.route('/my-account')
@login_required
def my_account():
    return render_template('my-account.html')


@app.route('/wishlist')
@login_required
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
            err_msg = "Vui lòng nhập đầy đủ thông tin"

    return render_template("login.html", err_msg=err_msg)


@app.route("/logout")
def logout():
    logout_user()

    return redirect(url_for("index",))


@app.route("/register", methods=["get", "post"])
def register():
    if session.get("user"):
        return redirect(request.url)

    err_msg = ""
    if request.method == "POST":
        try:
            name = request.form.get("name")
            username = request.form.get("username")
            password = request.form.get("password")
            confirm = request.form.get("confirm")
            email = request.form.get("email")
            if password.strip() != confirm.strip():
                err_msg = "Mat khau khong khop"
            else:
                if utils.add_user(name=name, username=username, email=email, password=password):
                    return redirect(url_for("email_verify", user_email=email))
                else:
                    err_msg = "Internal Error"
        except IntegrityError:
            err_msg = "Tên người dùng hoặc email đã có người sử dụng, vui lòng thử lại!"

    return render_template("register.html", err_msg=err_msg)


@app.route('/email-verification/<user_email>', methods=["GET", "POST"])
def email_verify(user_email):
    token = randomToken.dumps(user_email, salt="email_confirm")
    msg = Message('Thư xác nhận', sender='emailverifywebapp@gmail.com', recipients=[user_email])
    link = url_for('confirm_email', token=token, _external=True)
    msg.body = 'Vui lòng nhấn vào liên kết sau để xác nhận email. Liên kết của bạn là: {}'.format(link)
    mail.send(msg)
    return render_template("verify-email.html", user_email=user_email, )


@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = randomToken.loads(token, salt='email_confirm', max_age=900)
    except SignatureExpired:
        return render_template('verify-expired.html')
    return render_template('verify-success.html', email=email)


@app.route("/forgot_password", methods=["get", "post"])
def forgot_password():
    err_msg = ""
    if request.method == 'POST':
        try:
            email = request.form.get("email")
            if utils.check_mail(email=email):
                return redirect(url_for("request_sent", user_email=email))
            else:
                err_msg = "Nhập sai email"
        except IntegrityError:
            err_msg = "Nhập sai email"

    return render_template("forgot-password.html", err_msg=err_msg)


@app.route('/request_sent/<user_email>', methods=["GET", "POST"])
def request_sent(user_email):
    token = randomToken.dumps(user_email, salt="recovery_account")
    msg = Message('Khôi phục tài khoản', sender='emailverifywebapp@gmail.com', recipients=[user_email])
    link = url_for('recovery_account', token=token, _external=True)
    msg.body = 'Bạn đang tiến hành đặt lại mật khẩu, liên kết sẽ hết hạn sau 15 phút. Nhấn vào liên kết sau ' \
               'để đặt lại mật khẩu: {}'.format(link)
    mail.send(msg)
    return render_template("recovery-sent.html", user_email=user_email)


@app.route('/recovery_account/<token>')
def recovery_account(token):
    try:
        e = randomToken.loads(token, salt='recovery_account', max_age=900)
    except SignatureExpired:
        return render_template('verify-expired.html')
    return render_template('recovery-account.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000)
