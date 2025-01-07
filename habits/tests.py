from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from habits.models import Habit, Reminder
from users.models import User
from datetime import datetime, timedelta


class HabitTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="testuser@example.com")
        self.habit = Habit.objects.create(
            name='test_habbit',
            time='12:00:00',
            estimated_time=60,
            user=self.user,
            place="Home",
            action="Run",
            is_pleasant=False
        )
        self.reminder = Reminder.objects.create(
            habit=self.habit,
            remind_at=datetime.now() + timedelta(days=1),
            message="Test reminder message"
        )
        self.client.force_authenticate(user=self.user)


    def test_habit_creation_success(self):
        url = reverse("habits:habit-list")
        data = {
            "name": "New Habit",
            "time": "13:00:00",
            "estimated_time": 60,
            "user": self.user.pk,
            "place": "Gym",
            "action": "Workout",
            "is_pleasant": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)
        habit = Habit.objects.get(id=response.data["id"])
        self.assertEqual(habit.name, "New Habit")
        self.assertEqual(habit.time.strftime('%H:%M:%S'), "13:00:00")
        self.assertEqual(habit.place, "Gym")
        self.assertEqual(habit.action, "Workout")
        self.assertTrue(habit.is_pleasant)


    def test_habit_creation_failure_missing_name(self):
        url = reverse("habits:habit-list")
        data = {"time": "13:00:00", "estimated_time": 60}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)


    def test_habit_retrieval_success(self):
        url = reverse("habits:habit-detail", args=[self.habit.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.habit.name)


    def test_habit_update_success(self):
        url = reverse("habits:habit-detail", args=[self.habit.id])
        data = {
            "name": "Updated Habit",
            "time": "14:00:00",
            "estimated_time": 90,
            "place": "Park",
            "action": "Jogging",
            "user": self.user.pk,
            "is_pleasant": True,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.get(id=self.habit.id).name, "Updated Habit")


    def test_habit_deletion_success(self):
        url = reverse("habits:habit-detail", args=[self.habit.id])
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)