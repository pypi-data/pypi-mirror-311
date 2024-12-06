import logging

# Configure the logger
logging.basicConfig(filename="notification_audit.log", level=logging.INFO, format="%(asctime)s - %(message)s")

class NotificationAudit:
    
    """
    Logs sent notifications for accountability.
    """
    @staticmethod
    def log(recipient_email, subject):
        logging.info(f"Notification sent to {recipient_email}: {subject}")
