import smtplib

def send_email_otp(receiver_email, otp):
    sender_email = "your_email@gmail.com"
    sender_password = "osswajskxmqaehfr"  # NOT your normal password

    message = f"Subject: OTP Verification\n\nYour OTP is: {otp}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, message)
    server.quit()