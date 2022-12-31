from flask import Flask

from flask import make_response

from flask import jsonify

from flask import request

from flask_sqlalchemy import SQLAlchemy

from marshmallow import Schema, fields

import json

import os

BASE_DIR = os.path.dirname(__file__)
DB_FILE = os.path.join(BASE_DIR, "development.sqlite3")
SQLITE_DB_URI = "sqlite:///" + DB_FILE

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = SQLITE_DB_URI

db = SQLAlchemy(app)

class Framework(db.Model):
    __tablename__ = "frameworks"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):

        return f"Framework(id={self.id}, name={self.name})"

class FrameworkSchema(Schema):
    id = fields.Int()
    name = fields.Str()

framework_schema = FrameworkSchema()

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
def create_framework():
    framework = Framework.query.filter_by(
            name=request.json["name"]).first()

    if framework:

        return {
                "message": "Conflict",
                "status_code": 409
                }, 409

    new_framework = Framework(
            name=request.json["name"]
            )

    db.session.add(new_framework)
    db.session.commit()

    new_framework_dict = {
            "id": new_framework.id,
            "name": new_framework.name
            }

    return new_framework_dict

@app.route("/api/frameworks/<int:id>", methods=["PUT"])
def update_framework(id):
    framework = Framework.query.get(id)

    if not framework:

        return jsonify({
            "message": "Data not found",
            "status_code": 404
            }), 404

    framework.name = request.json["name"]

    db.session.commit()

    framework_json = framework_schema.dump(framework)

    return framework_json
    
@app.route("/api/frameworks/<int:id>", methods=["DELETE"])
def destroy_framework(id):
    framework = Framework.query.get(id)

    if framework:
        db.session.delete(framework)
        db.session.commit()

        return {}, 204
    else:

        return jsonify({
            "message": "Data not found",
            "status_code": 404
            }), 404

