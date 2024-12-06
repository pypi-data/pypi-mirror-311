class NotificationPayload:
    
    """
    Generates payloads for notifications based on events.
    """
    
    def __init__(self, recipient_email, subject, body):
        self.recipient_email = recipient_email
        self.subject = subject
        self.body = body

    @staticmethod
    def create(template_key, recipient_email, **context):
        """
        Create a notification payload using a predefined template.
        """
        template = TEMPLATES.get(template_key)
        if not template:
            raise ValueError(f"Template '{template_key}' not found.")
        subject, body = template.render(**context)
        return NotificationPayload(recipient_email, subject, body)
