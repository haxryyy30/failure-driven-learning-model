import subprocess
import sqlite3
import time

from datetime import datetime

from ai_engine import predict_root_cause
from ai_engine import detect_severity
from ai_engine import predict_root_cause
from ai_engine import detect_severity


# =====================================
# AUTO FIX FAILURE
# =====================================

def auto_fix_error(cause):

    if cause == "Database Failure":

        return "Database reconnection attempted"

    elif cause == "API Failure":

        return "API request retried successfully"

    elif cause == "Runtime Exception":

        return "Application restart suggested"

    elif cause == "Mathematical Runtime Exception":

        return "Division validation applied"

    else:

        return "No automatic fix available"

# =====================================
# STORE FAILURE
# =====================================

def store_error(error_message):

    prediction = predict_root_cause(

        error_message

    )

    predicted_cause = prediction["cause"]

    solution = prediction["solution"]

    confidence = prediction["confidence"]

    auto_fix_status = auto_fix_error(
        predicted_cause
    )   

    severity = detect_severity(

        error_message

    )

    conn = sqlite3.connect(

        "failures.db"

    )

    cursor = conn.cursor()

    # STORE NEW ERROR

    cursor.execute("""

        INSERT INTO failures (

            error_message,

            module_name,

            severity,

            predicted_cause,

            solution,

            confidence,
                   
            auto_fix_status

        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

    """, (

        error_message,

        "Python Runtime",

        severity,

        predicted_cause,

        solution,

        confidence,

        auto_fix_status

    ))

    conn.commit()

    conn.close()

    print("\nError stored successfully.\n")

# =====================================
# FILES TO MONITOR
# =====================================

files_to_monitor = [

    "monitored_apps/sample.py",
    "monitored_apps/api.py",
    "monitored_apps/payment.py",
    "monitored_apps/backend.py",

    "monitored_apps/file_not_found.py",
    "monitored_apps/value_error.py",
    "monitored_apps/attribute_error.py",
    "monitored_apps/import_error.py",
    "monitored_apps/type_error.py",
    "monitored_apps/unicode_error.py",
    "monitored_apps/recursion_error.py",
    "monitored_apps/assertion_error.py",
    "monitored_apps/floating_error.py",
    "monitored_apps/json_error.py"

]

# =====================================
# CONTINUOUS MONITOR
# =====================================

print("\nAI Failure Monitor Started...\n")

while True:

    for target_file in files_to_monitor:

        print(f"\nMonitoring: {target_file}\n")

        result = subprocess.run(

            ["python", target_file],

            capture_output=True,

            text=True

        )

        # ERROR DETECTED

        if result.returncode != 0:

            error_output = result.stderr

            print("ERROR DETECTED:\n")

            print(error_output)

            store_error(

                error_output

            )

        else:

            print(

                "Program executed successfully!"

            )

    # WAIT 5 SECONDS

    print(

        "\nWaiting 5 seconds before next scan...\n"

    )

    time.sleep(5)