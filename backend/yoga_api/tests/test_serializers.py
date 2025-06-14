from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Pose, BreathingExercise, Course, UserProfile
from ..serializers import (
    UserSerializer, PoseSerializer, BreathingExerciseSerializer,
    CourseSerializer, UserProfileSerializer
)

class SerializerTests(TestCase):

    def setUp(self):
        self.user_data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'password123'}
        self.user = User.objects.create_user(**self.user_data)

        self.pose1 = Pose.objects.create(name='Downward Dog', description='A foundational yoga pose.', difficulty='Intermediate')
        self.breathing_exercise1 = BreathingExercise.objects.create(name='Box Breathing', description='A calming breath technique.', duration_minutes=5)

        self.course_data_valid = {
            'title': 'Intro to Yoga',
            'description': 'A beginner friendly course.',
            'price': 19.99,
            'pose_ids': [self.pose1.id],
            'breathing_exercise_ids': [self.breathing_exercise1.id]
        }
        self.course = Course.objects.create(title="Existing Course", description="Desc", price=10.00)

        self.user_profile = UserProfile.objects.get(user=self.user) # Should exist due to signal

    def test_user_serializer_create(self):
        # Use different data than setUp to avoid unique username collision
        new_user_data = {'username': 'newserializeruser', 'email': 'newserializer@example.com', 'password': 'password123'}
        serializer = UserSerializer(data=new_user_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, new_user_data['username'])
        self.assertTrue(user.check_password(new_user_data['password']))

    def test_user_serializer_read(self):
        serializer = UserSerializer(instance=self.user)
        data = serializer.data
        self.assertEqual(data['username'], self.user.username)
        self.assertEqual(data['email'], self.user.email)
        self.assertNotIn('password', data) # Password should be write-only

    def test_pose_serializer(self):
        serializer = PoseSerializer(instance=self.pose1)
        data = serializer.data
        self.assertEqual(data['name'], self.pose1.name)

        new_pose_data = {'name': 'Childs Pose', 'description': 'Resting pose', 'difficulty': 'Beginner'}
        serializer = PoseSerializer(data=new_pose_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        pose = serializer.save()
        self.assertEqual(pose.name, new_pose_data['name'])

    def test_breathing_exercise_serializer(self):
        serializer = BreathingExerciseSerializer(instance=self.breathing_exercise1)
        data = serializer.data
        self.assertEqual(data['name'], self.breathing_exercise1.name)

        new_be_data = {'name': 'Nadi Shodhana', 'description': 'Alternate nostril breathing', 'duration_minutes': 10}
        serializer = BreathingExerciseSerializer(data=new_be_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        be = serializer.save()
        self.assertEqual(be.name, new_be_data['name'])

    def test_course_serializer_create(self):
        serializer = CourseSerializer(data=self.course_data_valid)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        course = serializer.save()
        self.assertEqual(course.title, self.course_data_valid['title'])
        self.assertEqual(course.poses.count(), 1)
        self.assertEqual(course.breathing_exercises.count(), 1)
        self.assertIn(self.pose1, course.poses.all())

    def test_course_serializer_read(self):
        self.course.poses.add(self.pose1)
        self.course.breathing_exercises.add(self.breathing_exercise1)
        serializer = CourseSerializer(instance=self.course)
        data = serializer.data
        self.assertEqual(data['title'], self.course.title)
        self.assertTrue(len(data['poses']) == 1) # Assuming related objects are serialized (read_only=True)
        self.assertEqual(data['poses'][0]['name'], self.pose1.name)
        self.assertTrue(len(data['breathing_exercises']) == 1)
        self.assertEqual(data['breathing_exercises'][0]['name'], self.breathing_exercise1.name)
        self.assertNotIn('pose_ids', data) # write_only field
        self.assertNotIn('breathing_exercise_ids', data) # write_only field


    def test_course_serializer_update(self):
        # Create a course first
        course_to_update = Course.objects.create(title="Initial Title", description="Desc", price=5.00)
        pose2 = Pose.objects.create(name="Warrior II", description="Strong pose", difficulty="Intermediate")

        update_data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'price': 15.00,
            'pose_ids': [pose2.id], # Update poses
            'breathing_exercise_ids': [] # Remove all breathing exercises
        }
        serializer = CourseSerializer(instance=course_to_update, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_course = serializer.save()

        self.assertEqual(updated_course.title, 'Updated Title')
        self.assertEqual(updated_course.poses.count(), 1)
        self.assertIn(pose2, updated_course.poses.all())
        self.assertEqual(updated_course.breathing_exercises.count(), 0)


    def test_user_profile_serializer_read(self):
        self.user_profile.enrolled_courses.add(self.course)
        serializer = UserProfileSerializer(instance=self.user_profile)
        data = serializer.data

        self.assertEqual(data['user']['username'], self.user.username)
        # Check for 'enrolled_courses_details' as 'enrolled_courses' is just IDs by default if not read_only with depth
        self.assertTrue('enrolled_courses_details' in data)
        self.assertEqual(len(data['enrolled_courses_details']), 1)
        self.assertEqual(data['enrolled_courses_details'][0]['title'], self.course.title)

    def test_serializer_required_fields(self):
        invalid_pose_data = {'description': 'Missing name and difficulty'}
        serializer = PoseSerializer(data=invalid_pose_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('difficulty', serializer.errors)

    # Add more tests for validation (e.g. data formats, choices on serializers if different from model)
    # and edge cases for each serializer.
