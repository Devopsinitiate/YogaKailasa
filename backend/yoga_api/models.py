from django.db import models
from django.contrib.auth.models import User

class Pose(models.Model):
    DIFFICULTY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    image_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class BreathingExercise(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    duration_minutes = models.PositiveIntegerField(help_text="Duration in minutes")

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    poses = models.ManyToManyField(Pose, related_name='courses', blank=True)
    breathing_exercises = models.ManyToManyField(BreathingExercise, related_name='courses', blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    enrolled_courses = models.ManyToManyField(Course, related_name='enrolled_users', blank=True)
    # Add other fields here if needed in the future, e.g.:
    # profile_picture_url = models.URLField(max_length=255, blank=True, null=True)
    # bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
