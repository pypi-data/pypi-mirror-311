from .notification_manager import NotificationManager


def send_notification(recipient, message):
    """
    A simple function to send a notification.
    """
    print(f"Notification sent to {recipient}: {message}")
