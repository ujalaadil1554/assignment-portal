
from flask import Flask, request, jsonify
import json
import os
from pathlib import Path

app = Flask(__name__)

REPORT_FILE = Path(__file__).resolve().parent / "testreport.json"


@app.route("/report", methods=["POST"])
def receive_report():
    expected_token = os.environ.get("REPORT_TOKEN")

    if not expected_token:
        return jsonify({
            "error": "Receiver token is not configured"
        }), 503

    provided_token = request.headers.get("X-Report-Token", "")

    if provided_token != expected_token:
        return jsonify({
            "error": "Unauthorized"
        }), 401

    report = request.get_json(silent=True)

    if not isinstance(report, dict):
        return jsonify({
            "error": "Invalid JSON report"
        }), 400

    required_fields = [
        "repository",
        "branch",
        "commit_sha",
        "run_id",
        "timestamp",
        "tests",
        "total_count",
        "passed_count",
        "failed_count",
        "overall_status"
    ]

    missing = [
        field for field in required_fields
        if field not in report
    ]

    if missing:
        return jsonify({
            "error": "Missing report fields",
            "fields": missing
        }), 400

    if not isinstance(report["tests"], list):
        return jsonify({
            "error": "Tests must be a list"
        }), 400

    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print("Report received and saved to testreport.json", flush=True)
    print("Commit:", report["commit_sha"], flush=True)
    print("Status:", report["overall_status"], flush=True)
    print(
        "Passed:",
        report["passed_count"],
        "/",
        report["total_count"],
        flush=True
    )

    return jsonify({
        "success": True,
        "message": "Report saved successfully"
    }), 200


if __name__ == "__main__":
    print("Report receiver running on http://localhost:5001/report")
    print("Reports will be saved to:", REPORT_FILE)
    app.run(host="127.0.0.1", port=5001)
