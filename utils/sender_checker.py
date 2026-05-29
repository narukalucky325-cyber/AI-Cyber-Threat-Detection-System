suspicious_keywords = [
    "secure-login",
    "verify-now",
    "account-update",
    "free-money"
]


def check_sender(sender_email):

    for word in suspicious_keywords:

        if word in sender_email:

            return True

    return False