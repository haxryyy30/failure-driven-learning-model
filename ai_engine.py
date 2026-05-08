# =====================================
# AI ROOT CAUSE ANALYSIS
# =====================================

def predict_root_cause(error_message):

    error = error_message.lower()

    # DATABASE

    if "database" in error:

        return {

            "cause": "Database Failure",

            "solution": "Check database server and credentials",

            "confidence": 95
        }

    # MEMORY

    elif "memory" in error:

        return {

            "cause": "Memory Overflow",

            "solution": "Optimize memory usage and close unused processes",

            "confidence": 97
        }

    # ZERO DIVISION

    elif "zerodivisionerror" in error:

        return {

            "cause": "Mathematical Runtime Exception",

            "solution": "Check denominator before division",

            "confidence": 92
        }

    # FILE NOT FOUND

    elif "filenotfounderror" in error:

        return {

            "cause": "Missing File",

            "solution": "Verify file path exists",

            "confidence": 88
        }

    # TIMEOUT

    elif "timeout" in error:

        return {

            "cause": "Network Timeout",

            "solution": "Check network stability",

            "confidence": 85
        }

    # API

    elif "api" in error:

        return {

            "cause": "API Failure",

            "solution": "Check API endpoint and authentication",

            "confidence": 90
        }

    # DEFAULT

    else:

        return {

            "cause": "Runtime Exception",

            "solution": "Check application logic and traceback",

            "confidence": 70
        }


# =====================================
# AUTO SEVERITY DETECTION
# =====================================

def detect_severity(error_message):

    error = error_message.lower()

    # HIGH

    if (

        "memory" in error
        or "database" in error
        or "unauthorized" in error
        or "kernel" in error
        or "crash" in error

    ):

        return "HIGH"

    # MEDIUM

    elif (

        "zerodivisionerror" in error
        or "timeout" in error
        or "runtime" in error
        or "overflow" in error

    ):

        return "MEDIUM"

    # LOW

    else:

        return "LOW"