def calculate_risk(email):
    
    score = 0
    reasons = []

    suspicious_keywords = {
        "urgent": 20,
        "password": 25,
        "verify": 20,
        "login": 15,
        "bank": 20,
        "click here": 15
    }

    email = email.lower()

    for word, points in suspicious_keywords.items():
        if word in email:
            score += points
            reasons.append(f"{word} detected")

    # Limit score to 100
    if score > 100:
        score = 100

    # Severity
    if score >= 70:
        severity = "HIGH"
    elif score >= 40:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return score, severity, reasons