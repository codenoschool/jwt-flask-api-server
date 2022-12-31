from flask import Flask

from flask import make_response

from flask import jsonify

from flask import request

import json

app = Flask(__name__)

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

