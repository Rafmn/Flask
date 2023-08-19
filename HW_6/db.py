from email.policy import default
from sqlite3 import connect
import databases
import sqlalchemy
from settings import settings

db = databases.Database(settings.DATABASE_URL)
mdt = sqlalchemy.MetaData()

products_db = sqlalchemy.Table('products', mdt,
                            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                            sqlalchemy.Column('model', sqlalchemy.String(48)),
                            sqlalchemy.Column('description', sqlalchemy.String(1000)),
                            sqlalchemy.Column('price', sqlalchemy.Float(15))
                            )

users_db = sqlalchemy.Table('users', mdt,
                            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                            sqlalchemy.Column('first_name', sqlalchemy.String(32)),
                            sqlalchemy.Column('last_name', sqlalchemy.String(48)),
                            sqlalchemy.Column('email', sqlalchemy.String(48)),
                            sqlalchemy.Column('password', sqlalchemy.String(128))
                            )

orders_db = sqlalchemy.Table('orders', mdt,
                            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                            sqlalchemy.Column('user_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')),
                            sqlalchemy.Column('product_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('products.id')),
                            sqlalchemy.Column('date_order', sqlalchemy.Date),
                            sqlalchemy.Column('status_order', sqlalchemy.Boolean, default=False)
                            )

engine = sqlalchemy.create_engine(
    settings.DATABASE_URL,
    connect_args = {'check_same_thread': False}
    )

mdt.create_all(engine)
