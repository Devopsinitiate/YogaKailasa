from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationView, UserLoginView,
    PoseViewSet, BreathingExerciseViewSet, CourseViewSet,
    InitiatePaymentView, VerifyPaymentView
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'poses', PoseViewSet, basename='pose')
router.register(r'breathing-exercises', BreathingExerciseViewSet, basename='breathingexercise')
router.register(r'courses', CourseViewSet, basename='course')

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('payment/initiate/', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('payment/verify/', VerifyPaymentView.as_view(), name='verify-payment'),
    path('', include(router.urls)), # Include the router URLs
]
