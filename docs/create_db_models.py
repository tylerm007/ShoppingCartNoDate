# created from response - used to create database and project
#  should run without error
#  if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func  # end imports from system/genai/create_db_models_inserts/create_db_models_prefix.py
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.orm import relationship
from datetime import date

logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)

    """
    description: Represents different categories in the store, such as 'Casual', 'Sports', 'Formal'.
    """


class Brand(Base):
    __tablename__ = 'brand'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    origin_country = Column(String)
    description = Column(String)

    """
    description: Contains details about different brands of golf shoes.
    """


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    size = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    brand_id = Column(Integer, ForeignKey('brand.id'))
    stock = Column(Integer, default=0)
    description = Column(String)

    """
    description: Represents individual golf shoes offered for sale, including price, size, and stock.
    """


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String)
    address = Column(String)

    """
    description: Contains customer data, such as name, email, and contact information.
    """


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    date_ordered = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float)
    status = Column(String, default='Pending')

    """
    description: Represents customer orders and includes order status and total amount.
    """


class OrderDetail(Base):
    __tablename__ = 'order_detail'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer, nullable=False)

    """
    description: Details of products in each order including quantity of each product.
    """


class Cart(Base):
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    """
    description: Stores information about shopping carts linked to individual customers.
    """


class CartItem(Base):
    __tablename__ = 'cart_item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey('cart.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer, nullable=False)

    """
    description: Represents products added to a customer's shopping cart with their quantities.
    """


class Payment(Base):
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    payment_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    amount = Column(Float, nullable=False)
    payment_method = Column(String)

    """
    description: Stores details of payments made for orders, including the payment method.
    """


class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    customer_id = Column(Integer, ForeignKey('customer.id'))
    rating = Column(Integer, nullable=False)
    comment = Column(String)
    review_date = Column(DateTime, default=datetime.utcnow)

    """
    description: Captures customer reviews and ratings for specific products.
    """


class Coupon(Base):
    __tablename__ = 'coupon'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, nullable=False)
    discount_percentage = Column(Float, nullable=False)
    expiry_date = Column(DateTime)
    description = Column(String)

    """
    description: Represents discount coupons that customers can apply to orders.
    """


class Wishlist(Base):
    __tablename__ = 'wishlist'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    """
    description: Stores lists of desired products by customers, often for future purchasing.
    """


class WishlistItem(Base):
    __tablename__ = 'wishlist_item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    wishlist_id = Column(Integer, ForeignKey('wishlist.id'))
    product_id = Column(Integer, ForeignKey('product.id'))

    """
    description: Keeps track of specific products contained in a customer's wishlist.
    """


# ALS/GenAI: Create an SQLite database
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
# ALS/GenAI: Prepare for sample data

# Assuming Base, engine, and session have been defined, and metadata created

# Populate Category Table
categories = [
    Category(name='Sports', description='Sports category for athletic use'),
    Category(name='Casual', description='Casual and everyday use'),
    Category(name='Formal', description='Formal shoes suitable for dress events'),
]

# Populate Brand Table
brands = [
    Brand(name='Nike', origin_country='USA', description='Leading sports brand'),
    Brand(name='Adidas', origin_country='Germany', description='Global sportswear manufacturer'),
    Brand(name='Puma', origin_country='Germany', description='Another top sportswear brand'),
]

# Populate Product Table
products = [
    Product(name='Nike Air Max', price=150.0, size=42, category_id=1, brand_id=1, stock=100),
    Product(name='Adidas Ultraboost', price=180.0, size=40, category_id=1, brand_id=2, stock=50),
    Product(name='Puma Suede Classic', price=85.0, size=43, category_id=2, brand_id=3, stock=70),
]

# Populate Customer Table
customers = [
    Customer(first_name='John', last_name='Doe', email='john.doe@example.com', phone='1234567890', address='123 Elm Street'),
    Customer(first_name='Jane', last_name='Smith', email='jane.smith@example.com', phone='0987654321', address='456 Oak Avenue'),
]

# Populate Order Table
orders = [
    Order(customer_id=1, total_amount=300.0, status='Completed'),
    Order(customer_id=2, total_amount=85.0, status='Pending'),
]

# Populate OrderDetail Table
order_details = [
    OrderDetail(order_id=1, product_id=1, quantity=2),
    OrderDetail(order_id=2, product_id=3, quantity=1),
]

# Populate Cart Table
carts = [
    Cart(customer_id=1),
    Cart(customer_id=2)
]

# Populate CartItem Table
cart_items = [
    CartItem(cart_id=1, product_id=1, quantity=1),
    CartItem(cart_id=2, product_id=2, quantity=3),
]

# Populate Payment Table
payments = [
    Payment(order_id=1, amount=300.0, payment_method='Credit Card'),
    Payment(order_id=2, amount=85.0, payment_method='PayPal'),
]

# Populate Review Table
reviews = [
    Review(product_id=1, customer_id=1, rating=5, comment='Great shoes, very comfortable.'),
    Review(product_id=2, customer_id=2, rating=4, comment='Good design, but runs small.'),
]

# Populate Coupon Table
coupons = [
    Coupon(code='DISCOUNT10', discount_percentage=10.0, expiry_date=datetime(2024, 12, 31)),
    Coupon(code='FREESHIP', discount_percentage=0.0, expiry_date=datetime(2025, 1, 31)),
]

# Populate Wishlist
wishlists = [
    Wishlist(customer_id=1, name='John’s Desired'),
    Wishlist(customer_id=2, name='Jane’s Picks'),
]

# Populate WishlistItem
wishlist_items = [
    WishlistItem(wishlist_id=1, product_id=2),
    WishlistItem(wishlist_id=2, product_id=1),
]

# Insert all data into the database
entities = categories + brands + products + customers + orders + order_details + carts + cart_items + payments + reviews + coupons + wishlists + wishlist_items

session.add_all(entities)
session.commit()


session.add_all([])
session.commit()
