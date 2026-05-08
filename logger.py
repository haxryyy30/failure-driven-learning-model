from database import connect_db

def log_failure(

    error_message,

    module_name,

    severity,

    predicted_cause,

    solution

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

        module_name,

        severity,

        predicted_cause,

        solution

    ))

    conn.commit()

    conn.close()