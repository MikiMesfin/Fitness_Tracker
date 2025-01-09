from django.db import models
from django.conf import settings

class ActivityType(models.TextChoices):
    RUNNING = 'RUNNING', 'Running'
    CYCLING = 'CYCLING', 'Cycling'
    WEIGHTLIFTING = 'WEIGHTLIFTING', 'Weightlifting'
    SWIMMING = 'SWIMMING', 'Swimming'
    YOGA = 'YOGA', 'Yoga'

class Activity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity_type = models.CharField(
        max_length=20,
        choices=ActivityType.choices,
    )
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    distance = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Distance in kilometers"
    )
    calories_burned = models.PositiveIntegerField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        app_label = 'activities'
        ordering = ['-date']
        verbose_name_plural = 'Activities'

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} on {self.date}"

class Goal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity_type = models.CharField(
        max_length=20,
        choices=ActivityType.choices,
    )
    target_value = models.DecimalField(max_digits=8, decimal_places=2)
    target_type = models.CharField(
        max_length=20,
        choices=[
            ('DISTANCE', 'Distance (km)'),
            ('DURATION', 'Duration (minutes)'),
            ('CALORIES', 'Calories Burned'),
        ]
    )
    start_date = models.DateField()
    end_date = models.DateField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s {self.activity_type} goal"

    class Meta:
        app_label = 'activities'
