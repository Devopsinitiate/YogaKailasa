from rest_framework import serializers
from .models import Pose, BreathingExercise, Course, UserProfile # Ensure UserProfile is imported
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

class UserProfileSerializer(serializers.ModelSerializer):
    # Making user read-only as it's set by the system (linked one-to-one)
    user = UserSerializer(read_only=True)
    # enrolled_courses = CourseSerializer(many=True, read_only=True)
    # Simpler representation for enrolled_courses to avoid deep nesting if not needed for profile view
    enrolled_courses_details = CourseSerializer(source='enrolled_courses', many=True, read_only=True)


    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'enrolled_courses', 'enrolled_courses_details']
        # enrolled_courses is writeable by ID (e.g. for admin or specific updates)
        # but typically updated via payment verification logic rather than direct profile update.
        # For this serializer, let's make enrolled_courses itself read-only for direct profile updates
        # and rely on other mechanisms (like payment verification) to modify it.
        read_only_fields = ['user', 'enrolled_courses', 'enrolled_courses_details']

# To make enrolled_courses writeable in UserProfileSerializer if needed (e.g. for admin):
# class UserProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     enrolled_courses = serializers.PrimaryKeyRelatedField(
#         many=True,
#         queryset=Course.objects.all(),
#         required=False
#     )
#     enrolled_courses_details = CourseSerializer(source='enrolled_courses', many=True, read_only=True)

#     class Meta:
#         model = UserProfile
#         fields = ['id', 'user', 'enrolled_courses', 'enrolled_courses_details']
#         read_only_fields = ['user', 'enrolled_courses_details']

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
