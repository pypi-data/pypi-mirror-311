import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

# Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class NotificationManager:
    """
    A manager for creating and sending notifications via email.
    """

    @staticmethod
    def generate_email_notification(recipient_email, subject, message, template_path=None, context=None):
        """
        Generate an email notification.
        
        Args:
            recipient_email (str): The recipient's email address.
            subject (str): The email subject.
            message (str): The email body text (if not using a template).
            template_path (str): Path to an HTML template (optional).
            context (dict): Context to populate the template (optional).

        Returns:
            MIMEText: An email message object ready to send.
        """
        if template_path:
            # Load and render template if provided
            try:
                with open(template_path, 'r') as template_file:
                    template = template_file.read()
                message = template.format(**context)
            except Exception as e:
                logger.error(f"Failed to load template: {e}")
                raise

        # Create email object
        email = MIMEMultipart()
        email['To'] = recipient_email
        email['Subject'] = subject
        email.attach(MIMEText(message, 'html'))

        return email

    @staticmethod
    def send_email_notification(email_message, smtp_server='smtp.example.com', smtp_port=587, sender_email='noreply@example.com', sender_password='password'):
        """
        Send the prepared email notification.

        Args:
            email_message (MIMEText): The email message to send.
            smtp_server (str): SMTP server to use.
            smtp_port (int): SMTP server port.
            sender_email (str): Email address of the sender.
            sender_password (str): Password for the sender email.

        Returns:
            bool: True if email was sent successfully, False otherwise.
        """
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, email_message['To'], email_message.as_string())
                logger.info(f"Email sent to {email_message['To']}")
                return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
