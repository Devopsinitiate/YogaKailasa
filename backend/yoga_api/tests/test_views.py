from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from unittest.mock import patch # For mocking Paystack API calls

from ..models import Pose, BreathingExercise, Course, UserProfile

class ViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key) # Authenticate client

        # Test data
        self.pose1 = Pose.objects.create(name='Downward Dog', description='A foundational yoga pose.', difficulty='Intermediate')
        self.breathing_exercise1 = BreathingExercise.objects.create(name='Box Breathing', description='A calming breath technique.', duration_minutes=5)
        self.course1 = Course.objects.create(title='Intro to Yoga', description='A beginner friendly course.', price=19.99)
        self.course1.poses.add(self.pose1)
        self.course1.breathing_exercises.add(self.breathing_exercise1)

        self.user_profile = UserProfile.objects.get(user=self.user) # Signal should have created this

    # Authentication Views Tests
    def test_user_registration_success(self):
        url = reverse('user-register')
        data = {'username': 'newuser', 'email': 'new@example.com', 'password': 'newpassword123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertIn('token', response.data) # Registration now returns token

    def test_user_registration_duplicate_username(self):
        url = reverse('user-register')
        data = {'username': 'testuser', 'email': 'another@example.com', 'password': 'newpassword123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_success(self):
        # Logout first if client is already authenticated by setUp
        self.client.credentials() # Clear credentials
        url = reverse('user-login')
        data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_login_failure(self):
        self.client.credentials() # Clear credentials
        url = reverse('user-login')
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_logout(self):
        url = reverse('user-logout')
        response = self.client.post(url, format='json') # Assumes client is authenticated
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify token is deleted (or try to use it and fail)
        self.assertFalse(Token.objects.filter(user=self.user).exists())


    # Content Views Tests (Poses, BreathingExercise, Course)
    def test_list_poses_unauthenticated(self):
        self.client.credentials() # Clear auth
        url = reverse('pose-list') # DefaultRouter generates names like 'modelname-list'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_create_pose_authenticated(self):
        url = reverse('pose-list')
        data = {'name': 'Warrior I', 'description': 'A standing pose.', 'difficulty': 'Beginner'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_pose_unauthenticated(self):
        self.client.credentials()
        url = reverse('pose-list')
        data = {'name': 'Warrior II', 'description': 'Another standing pose.', 'difficulty': 'Beginner'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # Or 403 if IsAuthenticatedOrReadOnly is default

    # Similar LIST and CREATE tests for BreathingExercise and Course
    def test_list_courses(self):
        url = reverse('course-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_retrieve_course(self):
        url = reverse('course-detail', kwargs={'pk': self.course1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.course1.title)

    # User Profile Views
    def test_retrieve_user_profile(self):
        url = reverse('user-profile-detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], self.user.username)

    def test_update_user_profile(self):
        # UserProfileSerializer is mostly read-only for user-facing updates,
        # but if we add writable fields like 'bio', this test would change them.
        # For now, it should just retrieve. An update might not change much.
        url = reverse('user-profile-detail')
        # Example: data = {'bio': 'Yoga enthusiast'}
        # response = self.client.patch(url, data, format='json')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.user_profile.refresh_from_db()
        # self.assertEqual(self.user_profile.bio, 'Yoga enthusiast')
        response = self.client.get(url) # Just retrieve again
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_list_enrolled_courses(self):
        self.user_profile.enrolled_courses.add(self.course1)
        url = reverse('user-enrolled-courses')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.course1.title)

    # Payment Views Tests (with mocking)
    @patch('yoga_api.views.Transaction.initialize')
    def test_initiate_payment_success(self, mock_initialize):
        mock_initialize.return_value = (
            200,
            "Success",
            {"authorization_url": "http://paystack.com/dummy_auth", "access_code": "dummy_access", "reference": "dummy_ref"}
        )
        url = reverse('initiate-payment')
        data = {'course_id': self.course1.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('authorization_url', response.data)
        mock_initialize.assert_called_once()

    def test_initiate_payment_unauthenticated(self):
        self.client.credentials() # Clear auth
        url = reverse('initiate-payment')
        data = {'course_id': self.course1.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('yoga_api.views.Transaction.verify')
    def test_verify_payment_success_and_enroll(self, mock_verify):
        mock_verify.return_value = (
            200,
            "Success",
            {"status": "success", "reference": "dummy_ref", "amount": int(self.course1.price * 100),
             "metadata": {"course_id": self.course1.id, "user_id": self.user.id}}
        )
        url = reverse('verify-payment') + '?reference=dummy_ref'
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Payment verified successfully and course enrolled", response.data.get("message", ""))

        self.user_profile.refresh_from_db()
        self.assertTrue(self.user_profile.enrolled_courses.filter(id=self.course1.id).exists())
        mock_verify.assert_called_once_with(reference='dummy_ref')

    @patch('yoga_api.views.Transaction.verify')
    def test_verify_payment_failure_from_paystack(self, mock_verify):
        mock_verify.return_value = (200, "Verification successful", {"status": "failed"}) # Paystack verified, but payment failed
        url = reverse('verify-payment') + '?reference=failed_ref'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK) # The API call itself is fine
        self.assertIn("payment was not completed", response.data.get("message", ""))

    def test_verify_payment_unauthenticated(self):
        self.client.credentials()
        url = reverse('verify-payment') + '?reference=some_ref'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Add more tests for other CRUD operations (RETRIEVE, UPDATE, DELETE) for each content model,
    # including permission checks (e.g., non-admin users cannot delete if not owner, etc.).
    # Example: test_delete_course_not_admin, test_update_own_pose (if ownership was a feature)
    # Also test edge cases like not found, invalid data for updates.
