import time
import sqlite3

from ai_model import predict_failure


# =========================
# DATABASE CONNECTION
# =========================

def connect_db():

    return sqlite3.connect('failures.db')


# =========================
# AI SOLUTION FUNCTION
# =========================

def suggest_solution(predicted_cause):

    solutions = {

        "Database Failure":
        "Check database server and credentials",

        "Null Error":
        "Validate objects before usage",

        "Memory Leak":
        "Optimize memory allocation",

        "Network Timeout":
        "Check network/API response",

        "Performance Issue":
        "Optimize CPU intensive tasks",

        "Security Issue":
        "Check authentication system",

        "Storage Issue":
        "Free disk space",

        "System Crash":
        "Restart affected services"

    }

    return solutions.get(
        predicted_cause,
        "Perform system diagnostics"
    )


# =========================
# AI SEVERITY DETECTION
# =========================

def detect_severity(error_message):

    error_message = error_message.lower()

    # HIGH SEVERITY

    if (

        "crash" in error_message
        or "kernel" in error_message
        or "database" in error_message
        or "unauthorized" in error_message
        or "failure" in error_message
        or "security" in error_message

    ):

        return "HIGH"

    # MEDIUM SEVERITY

    elif (

        "timeout" in error_message
        or "memory" in error_message
        or "cpu" in error_message
        or "overflow" in error_message
        or "slow" in error_message

    ):

        return "MEDIUM"

    # LOW SEVERITY

    else:

        return "LOW"


# =========================
# SAVE FAILURE TO DATABASE
# =========================

def save_failure(
    error_message,
    predicted_cause,
    solution,
    severity
):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO failures
    (
        error_message,
        module_name,
        severity,
        predicted_cause,
        solution
    )

    VALUES (?, ?, ?, ?, ?)

    """, (

        error_message,
        "Auto Monitor",
        severity,
        predicted_cause,
        solution

    ))

    conn.commit()

    conn.close()


# =========================
# START MONITOR
# =========================

processed_logs = set()

print("AI Log Monitor Started...")


# =========================
# CONTINUOUS LOG MONITORING
# =========================

while True:

    try:

        with open(
            'system.log',
            'r',
            encoding='utf-8'
        ) as file:

            logs = file.readlines()

        for log in logs:

            log = log.strip()

            # ONLY NEW LOGS

            if log not in processed_logs:

                processed_logs.add(log)

                # CHECK ERROR LOGS

                if "ERROR" in log:

                    error_message = log.replace(
                        "ERROR:",
                        ""
                    ).strip()

                    print(
                        f"\nDetected Error: {error_message}"
                    )

                    # AI PREDICTION

                    predicted_cause = predict_failure(
                        error_message
                    )

                    print(
                        f"AI Prediction: {predicted_cause}"
                    )

                    # SOLUTION

                    solution = suggest_solution(
                        predicted_cause
                    )

                    # SEVERITY

                    severity = detect_severity(
                        error_message
                    )

                    print(
                        f"Severity: {severity}"
                    )

                    # SAVE DATABASE

                    save_failure(
                        error_message,
                        predicted_cause,
                        solution,
                        severity
                    )

                    print(
                        "Saved to database"
                    )

        time.sleep(5)

    except Exception as e:

        print(f"Monitor Error: {e}")

        time.sleep(5)