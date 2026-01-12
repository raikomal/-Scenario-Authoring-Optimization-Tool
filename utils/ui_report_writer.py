import csv
import os
from datetime import datetime

REPORT_FILE = None
TASK_COUNTER = 0


def start_new_report():
    global REPORT_FILE, TASK_COUNTER
    TASK_COUNTER = 0

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    base_reports = os.path.join(os.getcwd(), "reports")
    csv_dir = os.path.join(base_reports, "csv")

    os.makedirs(csv_dir, exist_ok=True)

    REPORT_FILE = os.path.join(
        csv_dir,
        f"ui_test_report_{timestamp}.csv"
    )

    with open(REPORT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Project",
            "Application",
            "Micro_Application",
            "Title",
            "Description",
            "Steps",
            "Expected_Result",
            "Actual_Result",
            "Status",
            "Remark",
            "Task_ID"
        ])

    print(f"📄 New report started: {REPORT_FILE}")


def write_test_report(
    project,
    application,
    micro_application,
    title,
    description,
    steps,
    expected_result,
    actual_result,
    status,
    remark
):
    global REPORT_FILE, TASK_COUNTER

    if not REPORT_FILE:
        raise Exception("start_new_report() not called")

    TASK_COUNTER += 1

    with open(REPORT_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            project,
            application,
            micro_application,
            title,
            description,
            steps,
            expected_result,
            actual_result,
            status,
            remark,
            TASK_COUNTER
        ])


def write_fail_report(title, error_message):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    fail_dir = os.path.join(os.getcwd(), "reports", "failures")
    os.makedirs(fail_dir, exist_ok=True)

    filename = os.path.join(fail_dir, f"FAIL_{timestamp}.txt")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(title + "\n\n")
        f.write(error_message)
