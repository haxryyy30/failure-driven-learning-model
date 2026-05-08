import sqlite3


# =====================================
# CONNECT DATABASE
# =====================================

def connect_db():

    return sqlite3.connect("failures.db")


# =====================================
# LEARN FROM FAILURES
# =====================================

def learn_from_failures():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT
            error_message,
            COUNT(*) as frequency

        FROM failures

        GROUP BY error_message

        ORDER BY frequency DESC

    """)

    data = cursor.fetchall()

    conn.close()

    return data


# =====================================
# GET TOP PATTERNS
# =====================================

def get_top_patterns(limit=5):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT
            predicted_cause,
            COUNT(*) as total

        FROM failures

        GROUP BY predicted_cause

        ORDER BY total DESC

        LIMIT ?

    """, (limit,))

    patterns = cursor.fetchall()

    conn.close()

    return patterns


# =====================================
# UPDATE CONFIDENCE
# =====================================

def update_confidence(error_message):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT COUNT(*)

        FROM failures

        WHERE error_message = ?

    """, (error_message,))

    frequency = cursor.fetchone()[0]

    # AI LEARNING FORMULA

    confidence = min(50 + (frequency * 5), 99)

    conn.close()

    return confidence