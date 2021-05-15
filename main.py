import os
import uuid
from datetime import datetime

import dotenv
from cockroachdb.sqlalchemy import run_transaction
from flask import Flask, request
from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

from backend.vision import detect_objects, detect_logos

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


class OwnerAccount(Base):
    """
    The OwnerAccount class corresponds to the "owner_accounts" database table.
    Creating an account as an Owner is mandatory to create a store.
    """

    __tablename__ = "owner_accounts"
    username = Column(String, primary_key=True)
    password = Column(String)


class UserAccount(Base):
    """
    The UserAccount class corresponds to the "accounts" database table.
    Creating an account as User is mandatory to create a store.
    """

    __tablename__ = "user_accounts"
    username = Column(String, primary_key=True)
    password = Column(String)


class UserHistory(Base):
    """
    The UserHistory class corresponds to the "user_history" database table.
    It's going to have a list of stores each user checked in to.
    """

    __tablename__ = "user_history"
    username = Column(String, primary_key=True)
    store_id = Column(String)  # store ID
    time = Column(DateTime)  # time of check in


# Create an engine to communicate with the database. The
# "cockroachdb://" prefix for the engine URL indicates that we are
# connecting to CockroachDB using the 'cockroachdb' dialect.
engine = create_engine(
    os.environ.get("COCKROACHDB_URL"),
    echo=False,  # Don't log SQL queries to stdout
)

# Automatically create the tables based on all the classes defined above that inherit from "Base".
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

UPLOAD_FOLDER = os.path.join("uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def file_name(filename):
    return os.path.join(UPLOAD_FOLDER, filename)


@app.route("/")
def index():
    return "Hello user! What's up? <input></input>"


"""FUNCTIONALITY FOR OWNERS:"""


@app.route("/login_owner")
def login_owner():
    username = request.args.get("username")
    password = request.args.get("password")
    account = run(
        lambda sess: sess.query(OwnerAccount).filter_by(username=username)
    ).one()
    if account.password == password:
        # Success
        return "Success", 200
    else:
        return "Failure", 401


@app.route("/register_owner")
def register_owner():
    username = request.args.get("username")
    password = request.args.get("password")
    account = run(
        lambda sess: sess.query(OwnerAccount)
        .filter(exists().where(OwnerAccount.username == username))
        .all()
    )
    if len(account) > 0:
        # account with this username already exists
        return "Account for this Owner already exists!", 409
    else:
        run(lambda sess: sess.add(OwnerAccount(username=username, password=password)))
        return "Owner Account successfully created!", 200


# ? Takes parameter from frontend that specifies name of the store.
@app.route("/create_store")
def create_store():
    store_name = request.args.get("store_name")
    owner = request.args.get("owner")  # username of the owner.
    store_id = run(lambda s: insert_store(s, store_name, owner))
    print(f"Returned from run: {store_id}")
    return store_id, 200


"""FUNCTIONALITY FOR USERS:"""


@app.route("/user_history")
def user_history():
    username = request.args.get("username")
    pass


@app.route("/login_user")
def login_user():
    username = request.args.get("username")
    password = request.args.get("password")
    account = run(
        lambda sess: sess.query(UserAccount).filter_by(username=username)
    ).one()
    if account.password == password:
        # Success
        return "Success", 200
    else:
        return "Failure", 401


@app.route("/register_user")
def register_user():
    username = request.args.get("username")
    password = request.args.get("password")
    account = run(
        lambda sess: sess.query(UserAccount)
        .filter(exists().where(UserAccount.username == username))
        .all()
    )
    if len(account) > 0:
        # account with this username already exists
        return "Account for this User already exists!", 409
    else:
        run(lambda sess: sess.add(UserAccount(username=username, password=password)))
        return "User Account successfully created!", 200


# ? will contain a GET parameter (storeid) - the ID of the store to check into
@app.route("/check_in")
def method_name():
    username = request.args.get("username")
    storeid = request.args.get("storeid")
    run(
        lambda sess: sess.add(
            UserHistory(username=username, store_id=storeid, time=datetime.now())
        )
    )
    return {"storeid": storeid}, 200


@app.route("/detect_products", methods=["POST"])
def detect_products():
    image_file = request.files.get("products_image")
    fname, fext = os.path.splitext(image_file.filename)
    saved_filename = file_name(f"last_uploaded_image{fext}")
    image_file.save(saved_filename)

    print("Saved filename:", saved_filename)

    # now we have a path to the saved image, so we call the functions from vision.py
    print("Detecting objects now")
    objects = detect_objects(saved_filename)
    # print("Objects detected:", objects)

    print("Detecting logos now")
    logos = detect_logos(saved_filename)
    # print("Logos detected:", logos)

    return {
        "objects": [{"name": i.name, "confidence": i.score} for i in objects],
        "logos": [i.description for i in logos],
    }, 200


@app.route("/list_stores")
def list_stores():
    # query table of stores
    stores = run(lambda sess: sess.query(Store).all())
    print("List of stores returned:", "\n".join(map(repr, stores)))
    return {
        "stores": [{"id": i.id, "name": i.name, "owner": i.owner} for i in stores]
    }, 200


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 8080)))
