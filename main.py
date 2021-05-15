import os
import uuid

import dotenv
from cockroachdb.sqlalchemy import run_transaction
from flask import Flask, request
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

Base = declarative_base()

dotenv.load_dotenv()


class Store(Base):
    """The Store class corresponds to the "stores" database table."""

    __tablename__ = "stores"
    id = Column(String, primary_key=True)
    name = Column(String)
    owner = Column(String)  # username of the store owner.

    def __repr__(self):
        return str({"id": self.id, "name": self.name, "owner": self.owner})


class Product(Base):
    """The Product class corresponds to the "products" database table."""

    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    price = Column(Integer)


class Account(Base):
    """
    The Account class corresponds to the "accounts" database table.
    Creating an account is mandatory to create a store.
    """

    __tablename__ = "accounts"
    username = Column(String, primary_key=True)
    password = Column(String)


# Create an engine to communicate with the database. The
# "cockroachdb://" prefix for the engine URL indicates that we are
# connecting to CockroachDB using the 'cockroachdb' dialect.
engine = create_engine(
    os.environ.get("COCKROACHDB_URL"),
    echo=False,  # Don't log SQL queries to stdout
)
# Automatically create the tables based on the Store, Account and Product classes.
Base.metadata.create_all(engine)


def Session():
    return sessionmaker(bind=engine, autocommit=True, expire_on_commit=False)


def run(func):
    return run_transaction(Session(), func)


def insert_store(session, name, owner):
    new_id = str(uuid.uuid4())
    session.add(Store(id=new_id, name=name, owner=owner))
    return new_id


# ? initialise the Flask app
app = Flask(__name__)


@app.route("/")
def index():
    return "Hello user! What's up? <input></input>"


@app.route("/login")
def login():
    username = request.args.get("username")
    password = request.args.get("password")
    account = run(lambda sess: sess.query(Account).filter_by(username=username)).one()
    if account.password == password:
        # Success
        return "Success", 200
    else:
        return "Failure", 401


# GET parameters:
# @param username: Username to register with.
# @param password: Password.
@app.route("/register")
def register():
    username = request.args.get("username")
    password = request.args.get("password")
    account = run(
        lambda sess: sess.query(Account)
        .filter(exists().where(Account.username == username))
        .all()
    )
    if len(account) > 0:
        # account with this username already exists
        return "Account already exists!", 409
    else:
        run(lambda sess: sess.add(Account(username=username, password=password)))
        return "Account successfully created!", 200


@app.route("/list_stores")
def list_stores():
    # query table of stores
    stores = run(lambda sess: sess.query(Store).all())
    print("List of stores returned:", "\n".join(map(repr, stores)))
    return {
        "stores": [{"id": i.id, "name": i.name, "owner": i.owner} for i in stores]
    }, 200


# ? Takes parameter from frontend that specifies name of the store.
@app.route("/create_store")
def create_store():
    store_name = request.args.get("store_name")
    owner = request.args.get("owner")  # username of the owner.
    store_id = run(lambda s: insert_store(s, store_name, owner))
    print(f"Returned from run: {store_id}")
    return store_id, 200


# ? will contain a GET parameter (storeid) - the ID of the store to check into
@app.route("/check_in")
def method_name():
    storeid = request.args.get("storeid")
    return {"storeid": storeid}, 200


@app.route("/detect_objects", methods=["GET", "POST"])
def detect_object():
    pass


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 8080)))
