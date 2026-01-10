import csv
import os
from datetime import datetime

REPORT_FILE = None


def start_new_report():
    """
    Starts a fresh CSV report for each pytest run
    """
    global REPORT_FILE

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    REPORT_FILE = f"ui_test_report_{timestamp}.csv"

    with open(REPORT_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Product",
            "Module",
            "Feature",
            "Test Case",
            "Description",
            "Steps",
            "Expected Result",
            "Actual Result",
            "Status",
            "Remarks",
            "Task ID"
        ])

    print(f"📄 New report started: {REPORT_FILE}")


def write_test_report(
    product,
    module,
    feature,
    test_case,
    description,
    steps,
    expected,
    actual,
    status,
    remarks,
    task_id
):
    """
    Appends a test result row into the active report
    """
    global REPORT_FILE

    if not REPORT_FILE:
        raise Exception("❌ start_new_report() was not called before writing report")

    with open(REPORT_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            product,
            module,
            feature,
            test_case,
            description,
            steps,
            expected,
            actual,
            status,
            remarks,
            task_id
        ])


def write_fail_report(title, error_message):
    """
    Writes failure details in a separate fail log
    """
    with open("ui_failures.log", "a", encoding="utf-8") as file:
        file.write("\n" + "=" * 80 + "\n")
        file.write(f"{title}\n")
        file.write(str(error_message))
        file.write("\n" + "=" * 80 + "\n")
