
from flask import Flask, request, jsonify, send_from_directory
from urllib.parse import urlparse

app = Flask(__name__)

submissions = []


def is_valid_url(url):
    try:
        parsed = urlparse(url)
        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.hostname)
            and "." in parsed.hostname
            and not any(char.isspace() for char in url)
        )
    except ValueError:
        return False


@app.route("/")
def home():
    return send_from_directory("static", "index.html")


@app.route("/submit", methods=["POST"])
def submit_assignment():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "Invalid submission data"
        }), 400

    required_fields = {
        "name": "Student name",
        "reg_number": "Registration number",
        "title": "Assignment title",
        "url": "Submission URL"
    }

    for field, label in required_fields.items():
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            return jsonify({
                "success": False,
                "message": f"{label} is required"
            }), 400

    if not is_valid_url(data["url"]):
        return jsonify({
            "success": False,
            "message": "Invalid submission URL"
        }), 400

    submission = {
        field: data[field].strip()
        for field in required_fields
    }

    submissions.append(submission)

    return jsonify({
        "success": True,
        "message": "Assignment submitted successfully",
        "submission": submission
    }), 200


@app.route("/submissions", methods=["GET"])
def get_submissions():
    return jsonify(submissions), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
