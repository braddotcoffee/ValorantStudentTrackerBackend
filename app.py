from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS, cross_origin
from lib.not_found import NotFoundError
from lib.sheets import SheetsService

app = Flask(__name__)
CORS(app, support_credentials=True)

limiter = Limiter(
    get_remote_address, app=app, storage_uri="memory://", default_limits=["100 per day"]
)


@app.route("/list_students", methods=["GET"])
@cross_origin(support_credentials=True)
def list_students():
    result = SheetsService.fetch_students()
    return jsonify(result), 200


@app.route("/student", methods=["GET"])
@cross_origin(support_credentials=True)
def student():
    if request.args.get("name") is None:
        return "Bad Request", 400
    student_name = request.args["name"]
    try:
        student = SheetsService.fetch_student(student_name)
        return jsonify(student), 200
    except NotFoundError:
        return "Not Found", 404


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
