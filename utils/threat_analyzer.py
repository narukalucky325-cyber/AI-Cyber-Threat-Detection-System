def calculate_threat(phishing_confidence):

    if phishing_confidence >= 90:
        return "CRITICAL"

    elif phishing_confidence >= 70:
        return "HIGH"

    elif phishing_confidence >= 40:
        return "MEDIUM"

    else:
        return "LOW"