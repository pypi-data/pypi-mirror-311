class NotificationTemplate:
    """
    Handles creation and management of notification templates.
    """
    def __init__(self, subject, body):
        self.subject = subject
        self.body = body

    def render(self, **context):
        """
        Render the template with the given context.
        Example: render(driver_name="John", shipment_id="SH12345")
        """
        subject = self.subject.format(**context)
        body = self.body.format(**context)
        return subject, body

# Predefined templates
TEMPLATES = {
    "shipment_assigned": NotificationTemplate(
        subject="Shipment Assigned: {shipment_id}",
        body="Dear {driver_name},\n\nYou have been assigned to shipment {shipment_id} "
             "from {origin} to {destination}. The deadline is {deadline}. Please confirm.\n\nThank you!"
    ),
    "shipment_delayed": NotificationTemplate(
        subject="Shipment Delayed: {shipment_id}",
        body="Alert: Shipment {shipment_id} is delayed. Original deadline: {deadline}. "
             "Please coordinate with dispatchers.\n\nThank you!"
    ),
}
