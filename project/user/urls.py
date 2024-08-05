from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView # type: ignore
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('otp/', views.otpw, name='otp'),
    path('home/', views.home, name='home'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token'),
]