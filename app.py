from flask import Flask
from flask import make_response

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

