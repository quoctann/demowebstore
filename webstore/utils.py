import hashlib

from webstore import db
from webstore.models import User


def add_user(name, username, email, password):
    user = User(name=name,
                username=username,
                email=email,
                password=str(hashlib.md5(password.strip().encode("utf-8")).hexdigest()))
    db.session.add(user)
    db.session.commit()

    return user


def check_login(username, password):
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    return User.query.filter(User.username == username,
                             User.password == password).first()


def check_user(username):
    return User.query.filter(User.username == username).first()


def check_mail(email):
    return User.query.filter(User.email == email).first()
