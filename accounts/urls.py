from django.urls import path

from .api.views import SignUpAPIView

app_name = 'accounts'

urlpatterns = [
    path('api-auth/signup/', SignUpAPIView.as_view(), name='signup'),     
]