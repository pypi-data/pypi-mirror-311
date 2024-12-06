class NotificationHandler:
    @staticmethod
    def send_email(recipient, subject, message):
        print(f"Sending email to {recipient}: {subject} - {message}")

    @staticmethod
    def log_notification(message):
        print(f"Log: {message}")
