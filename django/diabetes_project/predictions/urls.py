from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("predict/", PredictionView.as_view(), name="predict"),
    path("predict/<int:prediction_id>/", PredictionView.as_view(), name="delete_prediction"), 
    path("predict/download-pdf/", DownloadPredictionPDFView.as_view(), name="download_pdf"),
    path('register/', RegisterView.as_view(), name='register'),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path("send-test-email/", send_test_email, name="send_test_email"),
    path("password-reset/request/", PasswordResetRequestView.as_view(), name="password_reset_request"),
    path("password-reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]
