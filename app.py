
from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)

limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="memory://",
    default_limits=["100 per day"]
)


@app.route("/list_students", methods=["GET"])
@cross_origin(support_credentials=True)
def list_students():
    return "Hello World!\n", 200

@app.route("/student", methods=["GET"])
@cross_origin(support_credentials=True)
def student():
    return "Hello World!\n", 200


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")