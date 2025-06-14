from django.contrib.auth.models import User
from rest_framework import generics, permissions, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.shortcuts import get_object_or_404
# For pypaystack2
from pypaystack2.api import Transaction, Customer
from pypaystack2.exceptions import PaystackAPIError
import uuid # For generating unique reference

from .models import Pose, BreathingExercise, Course, User # Ensure User is imported if needed for enrollment
from .serializers import UserSerializer, PoseSerializer, BreathingExerciseSerializer, CourseSerializer

# View for User Registration (from previous step)
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# View for User Login (generates token - from previous step)
class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

# ViewSets for CRUD operations
class PoseViewSet(viewsets.ModelViewSet):
    queryset = Pose.objects.all()
    serializer_class = PoseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Allow read for anyone, write for authenticated

class BreathingExerciseViewSet(viewsets.ModelViewSet):
    queryset = BreathingExercise.objects.all()
    serializer_class = BreathingExerciseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class InitiatePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        course_id = request.data.get('course_id')
        # amount = request.data.get('amount') # Amount should be fetched from the course model
        email = request.user.email

        if not course_id:
            return Response({"error": "Course ID is required"}, status=400)

        try:
            course = get_object_or_404(Course, id=course_id)
            amount_kobo = int(course.price * 100) # Paystack expects amount in kobo (or smallest currency unit)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)

        # Initialize Paystack Transaction API
        transaction_api = Transaction(secret_key=settings.PAYSTACK_SECRET_KEY)

        # Generate a unique reference for the transaction
        reference = f"yoga_course_{course_id}_{uuid.uuid4().hex[:10]}"

        try:
            # Callback URL should point to your frontend page that handles verification
            # This will be something like 'http://localhost:3000/payment/success' in development
            # For now, constructing it relative to backend's root, assuming frontend handles routing from there
            # or is on the same domain. A better way is to have FRONTEND_BASE_URL in settings.
            domain = request.build_absolute_uri('/')[:-1] # Get http://localhost:8000 (or similar) without trailing slash
            # A common setup is frontend on / and backend on /api. If so, this needs adjustment.
            # Assuming frontend is served by Django or at least on the same host/port for this relative path.
            # More robust: Use a fixed frontend URL from settings.
            # For this task, we'll assume /payment/success is a route handled by the frontend SPA.
            callback_url = f"{domain.replace('/api', '')}/payment/success/" # Simplistic, may need refinement

            response_data = transaction_api.initialize(
                email=email,
                amount=amount_kobo,
                reference=reference,
                callback_url=callback_url, # Ensure your frontend can handle this
                metadata={
                    "course_id": course_id,
                    "user_id": request.user.id,
                    "course_title": course.title
                }
            )
            # response_data is a tuple: (status_code, message, data_dict)
            # data_dict contains authorization_url, access_code, reference
            if response_data[0] == 200: # Check for successful API call (HTTP 200 OK)
                return Response(response_data[2]) # Return the data part which includes authorization_url
            else:
                return Response({"error": "Failed to initialize payment with Paystack", "details": response_data[1]}, status=500)

        except PaystackAPIError as e:
            return Response({"error": f"Paystack API Error: {str(e)}"}, status=500)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=500)


class VerifyPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated] # Or AllowAny if webhook is used by Paystack server

    def get(self, request, *args, **kwargs):
        reference = request.query_params.get('reference')
        if not reference:
            return Response({"error": "Payment reference is required"}, status=400)

        transaction_api = Transaction(secret_key=settings.PAYSTACK_SECRET_KEY)

        try:
            response_data = transaction_api.verify(reference=reference)
            # response_data is a tuple: (status_code, message, data_dict)
            # data_dict contains payment status, amount, metadata, etc.
            if response_data[0] == 200 and response_data[2].get('status') == 'success':
                # Payment successful
                # Here you would typically:
                # 1. Check if the transaction amount matches the course price from metadata or db.
                # 2. Mark the transaction as successful in your database.
                # 3. Enroll the user in the course.
                #    e.g., user = request.user; course_id = response_data[2]['metadata']['course_id']
                #    course = Course.objects.get(id=course_id)
                #    # Add logic for UserCourseEnrollment model or similar
                #    # For now, just return success
                return Response({
                    "message": "Payment verified successfully.",
                    "data": response_data[2]
                })
            elif response_data[0] == 200 and response_data[2].get('status') != 'success':
                 return Response({
                    "message": "Payment verification successful but payment was not completed.",
                    "status": response_data[2].get('status'),
                    "data": response_data[2]
                }, status=200) # Or 400 if you want to signal a "bad" outcome for client
            else:
                return Response({"error": "Payment verification failed with Paystack", "details": response_data[1]}, status=500)

        except PaystackAPIError as e:
            return Response({"error": f"Paystack API Error: {str(e)}"}, status=500)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=500)
