import schedule
import time
from threading import Thread

class NotificationScheduler:
    
    """
    Schedules notifications for specific events.
    """
    
    def __init__(self):
        self.jobs = []

    def schedule_notification(self, func, trigger_time):
        """
        Schedule a notification using the `schedule` library.
        `func`: Callable to send a notification.
        `trigger_time`: Time to trigger the notification (e.g., "10:30").
        """
        job = schedule.every().day.at(trigger_time).do(func)
        self.jobs.append(job)

    def start(self):
        """
        Start the scheduler in a separate thread.
        """
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(1)

        thread = Thread(target=run_scheduler, daemon=True)
        thread.start()
