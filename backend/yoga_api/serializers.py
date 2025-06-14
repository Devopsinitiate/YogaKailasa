from rest_framework import serializers
from .models import Pose, BreathingExercise, Course
from django.contrib.auth.models import User

# Serializer for User (from previous step, kept here for cohesiveness if needed, or can be in views.py)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class PoseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pose
        fields = ['id', 'name', 'description', 'difficulty', 'image_url']

class BreathingExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BreathingExercise
        fields = ['id', 'name', 'description', 'duration_minutes']

class CourseSerializer(serializers.ModelSerializer):
    poses = PoseSerializer(many=True, read_only=True)
    breathing_exercises = BreathingExerciseSerializer(many=True, read_only=True)

    # To allow updating ManyToManyFields with IDs during write operations
    pose_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Pose.objects.all(), source='poses', write_only=True, required=False
    )
    breathing_exercise_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=BreathingExercise.objects.all(), source='breathing_exercises', write_only=True, required=False
    )

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'poses', 'breathing_exercises', 'price', 'pose_ids', 'breathing_exercise_ids']
        read_only_fields = ['poses', 'breathing_exercises'] # Display these as nested, but write using IDs

    def create(self, validated_data):
        # Pop IDs for ManyToMany fields before creating the Course instance
        pose_data = validated_data.pop('poses', [])
        breathing_exercise_data = validated_data.pop('breathing_exercises', [])

        course = Course.objects.create(**validated_data)

        course.poses.set(pose_data)
        course.breathing_exercises.set(breathing_exercise_data)
        return course

    def update(self, instance, validated_data):
        # Pop IDs for ManyToMany fields before updating the Course instance
        pose_data = validated_data.pop('poses', None)
        breathing_exercise_data = validated_data.pop('breathing_exercises', None)

        instance = super().update(instance, validated_data)

        if pose_data is not None:
            instance.poses.set(pose_data)
        if breathing_exercise_data is not None:
            instance.breathing_exercises.set(breathing_exercise_data)

        return instance
