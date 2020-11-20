from sqlalchemy import Column, Integer, Float, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from webstore import db
from flask_login import UserMixin


class SampleBase(db.Model):
    __abstract__ = True

    id = Column(String(10), primary_key=True)
    name = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


class Category(SampleBase):
    __tablename__ = 'category'

    products = relationship('Product', backref='category', lazy=True)


class Product(SampleBase):
    __tablename__ = 'product'

    price = Column(Float, default=0)
    brand = Column(String(20))
    image = Column(String(100))
    screen = Column(String(70))
    camera = Column(String(50))
    cpu = Column(String(50))
    total = Column(Integer, default=0)
    category_id = Column(String(10), ForeignKey(Category.id), nullable=False)


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(50), nullable=False)
    username = Column(String(20), nullable=False, unique=True)
    email = Column(String(50), nullable=False)
    password = Column(String(40), nullable=False)
    active = Column(Boolean, default=True)
    role = Column(Integer, default=0)
    email_confirmed = Column(Boolean, default=False)


if __name__ == '__main__':
    db.create_all()
