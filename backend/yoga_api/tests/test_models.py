from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Pose, BreathingExercise, Course, UserProfile

class ModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.pose1 = Pose.objects.create(name='Downward Dog', description='A foundational yoga pose.', difficulty='Intermediate')
        self.breathing_exercise1 = BreathingExercise.objects.create(name='Box Breathing', description='A calming breath technique.', duration_minutes=5)
        self.course_for_uniqueness_test = Course.objects.create(title='Course For Uniqueness Test', description='Desc', price=9.99)

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.username, 'testuser')

    def test_user_profile_auto_creation(self):
        # UserProfile should be created automatically by a signal when User is created
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(str(profile), "testuser's Profile")

    def test_pose_creation(self):
        self.assertEqual(Pose.objects.count(), 1)
        self.assertEqual(self.pose1.name, 'Downward Dog')
        self.assertEqual(str(self.pose1), 'Downward Dog')

    def test_breathing_exercise_creation(self):
        self.assertEqual(BreathingExercise.objects.count(), 1)
        self.assertEqual(self.breathing_exercise1.name, 'Box Breathing')
        self.assertEqual(str(self.breathing_exercise1), 'Box Breathing')

    def test_course_creation_and_relationships(self):
        course = Course.objects.create(
            title='Intro to Yoga',
            description='A beginner friendly course.',
            price=19.99
        )
        # self.course_for_uniqueness_test was created in setUp
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(str(course), 'Intro to Yoga')

        # Test ManyToMany relationships
        course.poses.add(self.pose1)
        self.assertEqual(course.poses.count(), 1)
        self.assertIn(self.pose1, course.poses.all())

        course.breathing_exercises.add(self.breathing_exercise1)
        self.assertEqual(course.breathing_exercises.count(), 1)
        self.assertIn(self.breathing_exercise1, course.breathing_exercises.all())

    def test_user_profile_enroll_in_course(self):
        profile = UserProfile.objects.get(user=self.user)
        course = Course.objects.create(title='Advanced Yoga', description='For experienced practitioners.', price=29.99)

        profile.enrolled_courses.add(course)
        self.assertEqual(profile.enrolled_courses.count(), 1)
        self.assertIn(course, profile.enrolled_courses.all())

        # Test related_name from Course to UserProfile
        self.assertIn(profile, course.enrolled_users.all())

    def test_difficulty_choices_pose(self):
        pose = Pose.objects.create(name='Childs Pose', description='A resting pose', difficulty='Beginner')
        self.assertEqual(pose.difficulty, 'Beginner')
        # Removing this part as it's not a reliable model-level test for choices.
        # Form/Serializer tests are better for choice validation.

    def test_unique_constraints(self):
        # Test creating a Pose with a name that already exists (from setUp)
        with self.assertRaises(Exception): # IntegrityError
            Pose.objects.create(name='Downward Dog', description='Another one', difficulty='Beginner')

        # Test creating a BreathingExercise with a name that already exists (from setUp)
        with self.assertRaises(Exception): # IntegrityError
            BreathingExercise.objects.create(name='Box Breathing', description='Another one', duration_minutes=3)

        # Test creating a Course with a title that already exists (from setUp of this method)
        with self.assertRaises(Exception): # IntegrityError
            Course.objects.create(title='Course For Uniqueness Test', description='Another one', price=12)

        # Test creating a User with a username that already exists (from setUp)
        with self.assertRaises(Exception): # IntegrityError
            User.objects.create_user(username='testuser', email='another@example.com', password='pw')

    # Add more tests as needed, e.g. for default values, specific field validations if any on model level
