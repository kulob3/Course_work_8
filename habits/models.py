from django.db import models
from config import settings


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={"is_pleasant": True},
    )
    reward = models.CharField(max_length=255, null=True, blank=True)
    frequency = models.PositiveIntegerField(default=1)
    estimated_time = models.PositiveIntegerField(help_text="Время в секундах")
    is_public = models.BooleanField(default=False)
    tg_nick = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="telegram nickname",
        blank=True,
        null=True,
        help_text="Required. 50 characters or fewer. Letters, digits and _ only.",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="avatar",
        help_text="Optional. Image file.",
    )
    tg_chat_id = models.CharField(
        max_length=50, verbose_name="telegram chat id", blank=True, null=True
    )

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.reward and self.related_habit:
            raise ValidationError("Cannot have both a reward and a related habit.")

        if self.estimated_time > 120:
            raise ValidationError("Estimated time must be 120 seconds or less.")

        if self.frequency > 7:
            raise ValidationError("Frequency must be at least once every 7 days.")

        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError(
                "Pleasant habits cannot have rewards or related habits."
            )

    def __str__(self):
        return f"{self.action} at {self.time} in {self.place}"


class Reminder(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    remind_at = models.DateTimeField()
    message = models.CharField(max_length=255)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Reminder for {self.habit.name} at {self.remind_at}"
