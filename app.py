from flask import Flask

from flask import make_response

from flask import jsonify

from flask import request

from flask_sqlalchemy import SQLAlchemy

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

    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):

        return f"Framework(id={self.id}, name={self.name})"

frameworks = [
        {
            "id": 1,
            "name": "Flask"
            },
        {
            "id": 2,
            "name": "Angular"
            },
        {
            "id": 3,
            "name": "Laravel"
            },
        ]

ID = 4

@app.route("/api/frameworks", methods=["GET"])
def get_frameworks():
    frameworks_json = json.dumps(
            frameworks,
            indent=4,
            separators=(", ", ": ")
            )

    response = make_response(
            frameworks_json,
            200)
    response.headers["Content-Type"] = "application/json"

    return response

@app.route("/api/frameworks/<int:id>")
def get_framework(id):
    framework = {}
    for f in frameworks:
        if f["id"] == id:
            framework = f
            break

    return jsonify(framework)

@app.route("/api/frameworks", methods=["POST"])
def create_framework():
    global ID

    new_framework = {
            "id": ID,
            "name": request.json["name"]
            }

    frameworks.append(new_framework)

    ID += 1

    return new_framework

@app.route("/api/frameworks/<int:id>", methods=["PUT"])
def update_framework(id):
    framework = [f for f in frameworks if f["id"] == id]

    if framework:
        framework = framework[0]
        framework["name"] = request.json["name"]

        return framework
    else:

        return jsonify({
            "message": "Data not found",
            "status_code": 404
            }), 404

@app.route("/api/frameworks/<int:id>", methods=["DELETE"])
def destroy_framework(id):
    framework = [f for f in frameworks if f["id"] == id]

    if framework:
        framework = framework[0]

        frameworks.remove(framework)

        return {}, 204
    else:

        return jsonify({
            "message": "Data not found",
            "status_code": 404
            }), 404

