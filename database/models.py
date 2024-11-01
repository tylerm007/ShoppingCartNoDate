# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  November 01, 2024 13:43:22
# Database: sqlite:////tmp/tmp.MpsT2AUaqw/ShoppingCartNoDate/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Brand(SAFRSBaseX, Base):
    __tablename__ = 'brand'
    _s_collection_name = 'Brand'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    origin_country = Column(String)
    description = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    ProductList : Mapped[List["Product"]] = relationship(back_populates="brand")



class Category(SAFRSBaseX, Base):
    __tablename__ = 'category'
    _s_collection_name = 'Category'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    ProductList : Mapped[List["Product"]] = relationship(back_populates="category")



class Coupon(SAFRSBaseX, Base):
    __tablename__ = 'coupon'
    _s_collection_name = 'Coupon'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False)
    discount_percentage = Column(Float, nullable=False)
    expiry_date = Column(DateTime)
    description = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)



class Customer(SAFRSBaseX, Base):
    __tablename__ = 'customer'
    _s_collection_name = 'Customer'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String)
    address = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    CartList : Mapped[List["Cart"]] = relationship(back_populates="customer")
    OrderList : Mapped[List["Order"]] = relationship(back_populates="customer")
    WishlistList : Mapped[List["Wishlist"]] = relationship(back_populates="customer")
    ReviewList : Mapped[List["Review"]] = relationship(back_populates="customer")



class Cart(SAFRSBaseX, Base):
    __tablename__ = 'cart'
    _s_collection_name = 'Cart'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customer.id'))
    created_at = Column(DateTime)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("CartList"))

    # child relationships (access children)
    CartItemList : Mapped[List["CartItem"]] = relationship(back_populates="cart")



class Order(SAFRSBaseX, Base):
    __tablename__ = 'order'
    _s_collection_name = 'Order'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customer.id'))
    date_ordered = Column(DateTime)
    total_amount = Column(Float)
    status = Column(String)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("OrderList"))

    # child relationships (access children)
    OrderDetailList : Mapped[List["OrderDetail"]] = relationship(back_populates="order")
    PaymentList : Mapped[List["Payment"]] = relationship(back_populates="order")



class Product(SAFRSBaseX, Base):
    __tablename__ = 'product'
    _s_collection_name = 'Product'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    size = Column(Integer, nullable=False)
    category_id = Column(ForeignKey('category.id'))
    brand_id = Column(ForeignKey('brand.id'))
    stock = Column(Integer)
    description = Column(String)

    # parent relationships (access parent)
    brand : Mapped["Brand"] = relationship(back_populates=("ProductList"))
    category : Mapped["Category"] = relationship(back_populates=("ProductList"))

    # child relationships (access children)
    CartItemList : Mapped[List["CartItem"]] = relationship(back_populates="product")
    OrderDetailList : Mapped[List["OrderDetail"]] = relationship(back_populates="product")
    ReviewList : Mapped[List["Review"]] = relationship(back_populates="product")
    WishlistItemList : Mapped[List["WishlistItem"]] = relationship(back_populates="product")



class Wishlist(SAFRSBaseX, Base):
    __tablename__ = 'wishlist'
    _s_collection_name = 'Wishlist'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customer.id'))
    name = Column(String, nullable=False)
    created_at = Column(DateTime)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("WishlistList"))

    # child relationships (access children)
    WishlistItemList : Mapped[List["WishlistItem"]] = relationship(back_populates="wishlist")



class CartItem(SAFRSBaseX, Base):
    __tablename__ = 'cart_item'
    _s_collection_name = 'CartItem'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    cart_id = Column(ForeignKey('cart.id'))
    product_id = Column(ForeignKey('product.id'))
    quantity = Column(Integer, nullable=False)

    # parent relationships (access parent)
    cart : Mapped["Cart"] = relationship(back_populates=("CartItemList"))
    product : Mapped["Product"] = relationship(back_populates=("CartItemList"))

    # child relationships (access children)



class OrderDetail(SAFRSBaseX, Base):
    __tablename__ = 'order_detail'
    _s_collection_name = 'OrderDetail'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('order.id'))
    product_id = Column(ForeignKey('product.id'))
    quantity = Column(Integer, nullable=False)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("OrderDetailList"))
    product : Mapped["Product"] = relationship(back_populates=("OrderDetailList"))

    # child relationships (access children)



class Payment(SAFRSBaseX, Base):
    __tablename__ = 'payment'
    _s_collection_name = 'Payment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('order.id'))
    payment_date = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("PaymentList"))

    # child relationships (access children)



class Review(SAFRSBaseX, Base):
    __tablename__ = 'review'
    _s_collection_name = 'Review'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey('product.id'))
    customer_id = Column(ForeignKey('customer.id'))
    rating = Column(Integer, nullable=False)
    comment = Column(String)
    review_date = Column(DateTime)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("ReviewList"))
    product : Mapped["Product"] = relationship(back_populates=("ReviewList"))

    # child relationships (access children)



class WishlistItem(SAFRSBaseX, Base):
    __tablename__ = 'wishlist_item'
    _s_collection_name = 'WishlistItem'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    wishlist_id = Column(ForeignKey('wishlist.id'))
    product_id = Column(ForeignKey('product.id'))

    # parent relationships (access parent)
    product : Mapped["Product"] = relationship(back_populates=("WishlistItemList"))
    wishlist : Mapped["Wishlist"] = relationship(back_populates=("WishlistItemList"))

    # child relationships (access children)
