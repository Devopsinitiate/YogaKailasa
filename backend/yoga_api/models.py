from django.db import models

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
