from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Activity, Goal
from datetime import date, timedelta

User = get_user_model()

class ActivityTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        self.client.force_authenticate(user=self.user)
        
        self.activity_data = {
            'activity_type': 'RUNNING',
            'duration': 30,
            'distance': 5.2,
            'calories_burned': 300,
            'date': date.today().isoformat(),
            'notes': 'Morning run'
        }

    def test_create_activity(self):
        url = reverse('activity-list')
        response = self.client.post(url, self.activity_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)
        self.assertEqual(Activity.objects.get().user, self.user)

    def test_list_activities(self):
        # Create some activities
        Activity.objects.create(user=self.user, **self.activity_data)
        
        url = reverse('activity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_activity_statistics(self):
        # Create multiple activities
        Activity.objects.create(user=self.user, **self.activity_data)
        self.activity_data['date'] = (date.today() + timedelta(days=1)).isoformat()
        Activity.objects.create(user=self.user, **self.activity_data)

        url = reverse('activity-statistics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_activities'], 2)
        self.assertEqual(response.data['total_duration'], 60)
        self.assertEqual(response.data['total_calories'], 600)

class GoalTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123!'
        )
        self.client.force_authenticate(user=self.user)
        
        self.goal_data = {
            'activity_type': 'RUNNING',
            'target_value': 100.0,
            'target_type': 'DISTANCE',
            'start_date': date.today().isoformat(),
            'end_date': (date.today() + timedelta(days=30)).isoformat()
        }

    def test_create_goal(self):
        url = reverse('goal-list')
        response = self.client.post(url, self.goal_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Goal.objects.count(), 1)
        self.assertEqual(Goal.objects.get().user, self.user)

    def test_goal_progress(self):
        # Create a goal
        goal = Goal.objects.create(user=self.user, **self.goal_data)
        
        # Create some activities that contribute to the goal
        activity_data = {
            'activity_type': 'RUNNING',
            'duration': 30,
            'distance': 10.0,
            'calories_burned': 300,
            'date': date.today(),
            'user': self.user
        }
        Activity.objects.create(**activity_data)
        
        url = reverse('goal-detail', args=[goal.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['progress']['current'], 10.0)
        self.assertEqual(response.data['progress']['percentage'], 10.0)
