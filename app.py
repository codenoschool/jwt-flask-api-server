from flask import Flask

from flask import make_response

from flask import jsonify

from flask import request

from flask_sqlalchemy import SQLAlchemy

from marshmallow import Schema, fields

from werkzeug.security import generate_password_hash, \
        check_password_hash
from datetime import datetime, timezone, timedelta

import json

import os

import jwt

import functools

BASE_DIR = os.path.dirname(__file__)
DB_FILE = os.path.join(BASE_DIR, "development.sqlite3")
SQLITE_DB_URI = "sqlite:///" + DB_FILE

app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = SQLITE_DB_URI

app.config["SECRET_KEY"] = "sk"

db = SQLAlchemy(app)

def jwt_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        try:
            decoded_jwt = jwt.decode(
                    request.headers["JWT"],
                    app.config["SECRET_KEY"],
                    algorithms=["HS256"]
                    )

            user = User.query.get(decoded_jwt["user_id"])

            if not user:

                return jsonify({
                    "message": "Data not found",
                    "status_code": 404
                    }), 404
        except jwt.exceptions.ExpiredSignatureError:

            return {
                    "message": "Login time-out",
                    "status_code": 440
                    }, 440
        except:

            return {
                    "message": "Forbidden",
                    "status_code": 403
                    }, 403

        return view(decoded_jwt, user, **kwargs)

    return wrapped_view

class Framework(db.Model):
    __tablename__ = "frameworks"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), unique=True)

    author_id = db.Column(db.ForeignKey("users.id"), nullable=False)

    def __init__(self, name, author_id):
        self.name = name
        self.author_id = author_id

    def __repr__(self):

        return f"Framework(id={self.id}, name={self.name})"

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(88), nullable=True)

    def hash_password(self, password):

        return generate_password_hash(
                password,
                method="sha256"
                )

    def check_password(self, password):

        return check_password_hash(
                self.password,
                password)

    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_password(password)

    def __repr__(self):

        return f"User(id={self.id}, username={self.username})"


class FrameworkSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    author_id = fields.Int()

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()

framework_schema = FrameworkSchema()
user_schema = UserSchema()

@app.route("/api/frameworks", methods=["GET"])
def get_frameworks():
    frameworks = Framework.query.all()

    frameworks_json = framework_schema.dump(frameworks, many=True)

    response = make_response(
            frameworks_json,
            200)
    response.headers["Content-Type"] = "application/json"

    return response

@app.route("/api/frameworks/<int:id>")
def get_framework(id):
    framework = Framework.query.get(id)

    if not framework:

        return jsonify({
            "message": "Data not found",
            "status_code": 404
            }), 404

    framework_json = framework_schema.dump(framework)

    return framework_json

@app.route("/api/frameworks", methods=["POST"])
@jwt_required
def create_framework(decoded_jwt, user):
    framework = Framework.query.filter_by(
            name=request.json["name"]).first()

    if framework:

        return {
                "message": "Conflict",
                "status_code": 409
                }, 409

    new_framework = Framework(
            name=request.json["name"],
            author_id=user.id
            )

    db.session.add(new_framework)
    db.session.commit()

    new_framework_dict = framework_schema.dump(new_framework)

    return new_framework_dict

@app.route("/api/frameworks/<int:id>", methods=["PUT"])
@jwt_required
def update_framework(decoded_jwt, user, id):
    framework = Framework.query.get(id)

    if not framework:

        return jsonify({
            "message": "Data not found",
            "status_code": 404
            }), 404

    if framework.author_id != user.id:
        return {
            "message": "Forbidden",
            "status_code": 403
            }, 403

    framework.name = request.json["name"]

    db.session.commit()

    framework_json = framework_schema.dump(framework)

    return framework_json
    
@app.route("/api/frameworks/<int:id>", methods=["DELETE"])
@jwt_required
def destroy_framework(decoded_jwt, user, id):
    framework = Framework.query.get(id)

    if framework:
        if framework.author_id != user.id:
            return {
                "message": "Forbidden",
                "status_code": 403
                }, 403

        db.session.delete(framework)
        db.session.commit()

        return {}, 204
    else:

        return jsonify({
            "message": "Data not found",
            "status_code": 404
            }), 404

@app.route("/api/users", methods=["POST"])
def create_user():
    user = User.query.filter_by(
            username=request.json["username"]).first()

    if user:

        return {
                "message": "Conflict",
                "status_code": 409
                }, 409

    new_user = User(
            username=request.json["username"],
            password=request.json["password"]
            )

    db.session.add(new_user)
    db.session.commit()

    new_user_json = user_schema.dump(new_user)

    return new_user_json

@app.route("/login", methods=["POST"])
def login():
    user = User.query.filter_by(
            username=request.json["username"]).first()

    if user and user.check_password(
            request.json["password"]):
        encoded_jwt = jwt.encode(
                {
                    "iss": user.username,
                    "user_id": user.id,
                    "exp": datetime.now(
                        tz=timezone.utc
                        ) + timedelta(minutes=2)
                    },
                app.config["SECRET_KEY"],
                algorithm="HS256"
                )
                    
        return jsonify({
            "JWT": encoded_jwt
            })
    else:

        return jsonify({
            "message": "Data not found",
            "status_code": 404
            }), 404

