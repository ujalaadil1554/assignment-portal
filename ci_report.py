
import json
import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

import requests


def create_report():
    xml_file = Path("pytest-results.xml")

    if not xml_file.exists():
        print("ERROR: pytest-results.xml not found")
        sys.exit(1)

    root = ET.parse(xml_file).getroot()

    tests = []

    for case in root.iter("testcase"):
        name = (
            case.get("classname", "") +
            "::" +
            case.get("name", "")
        )

        failure = case.find("failure")
        error = case.find("error")
        skipped = case.find("skipped")

        if failure is not None or error is not None:
            result = "failed"
            problem = failure if failure is not None else error
            failure_message = (
                problem.get("message", "") +
                "\n" +
                (problem.text or "")
            ).strip()

        elif skipped is not None:
            result = "skipped"
            failure_message = ""

        else:
            result = "passed"
            failure_message = ""

        tests.append({
            "name": name,
            "result": result,
            "failure_message": failure_message
        })

    passed = sum(t["result"] == "passed" for t in tests)
    failed = sum(t["result"] == "failed" for t in tests)
    skipped = sum(t["result"] == "skipped" for t in tests)

    report = {
        "repository": os.getenv("GITHUB_REPOSITORY", "local"),
        "branch": os.getenv("GITHUB_REF_NAME", "local"),
        "commit_sha": os.getenv("GITHUB_SHA", "local"),
        "run_id": os.getenv("GITHUB_RUN_ID", "local"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tests": tests,
        "total_count": len(tests),
        "passed_count": passed,
        "failed_count": failed,
        "skipped_count": skipped,
        "overall_status": (
            "passed"
            if failed == 0 and skipped == 0 and len(tests) > 0
            else "failed"
        )
    }

    return report


def main():
    report = create_report()

    print(json.dumps(report, indent=2))

    receiver_url = os.getenv("RECEIVER_URL", "").rstrip("/")
    token = os.getenv("REPORT_TOKEN", "")

    if not receiver_url or not token:
        print("ERROR: RECEIVER_URL or REPORT_TOKEN missing")
        sys.exit(1)

    response = requests.post(
        receiver_url + "/report",
        json=report,
        headers={"X-Report-Token": token},
        timeout=30
    )

    response.raise_for_status()

    print("Report delivered successfully!")


if __name__ == "__main__":
    main()
