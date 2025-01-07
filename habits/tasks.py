from celery import shared_task
import requests
from django.utils import timezone
from requests import RequestException

from config.settings import TELEGRAM_TOKEN
from habits.models import Reminder
import logging

logger = logging.getLogger(__name__)


# @shared_task
# def send_telegram_message(chat_id, text):
#     try:
#         token = TELEGRAM_TOKEN
#         url = f"https://api.telegram.org/bot{token}/sendMessage"
#         data = {"chat_id": chat_id, "text": text}
#         requests.post(url, data=data)
#     except Exception as e:
#         logger.error(f"Failed to send message to chat_id {chat_id}: {e}")

@shared_task(
    autoretry_for=(RequestException,),
    retry_backoff=True,
    retry_kwargs={'max_retries': 5},
)
def send_telegram_message(chat_id, text):
    token = TELEGRAM_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    response = requests.post(url, data=data)
    response.raise_for_status()

@shared_task
def check_reminders():
    now = timezone.now()
    reminders = Reminder.objects.filter(remind_at__lte=now, sent=False)
    for reminder in reminders:
        send_telegram_message.delay(
            reminder.habit.user.telegram_chat_id, reminder.message
        )
        reminder.sent = True
        reminder.save()


@shared_task
def test_send_telegram_message():
    chat_id = "249799516"
    text = "This is a test message"
    send_telegram_message(chat_id, text)
