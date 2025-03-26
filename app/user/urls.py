from django.urls import path

from user import views

# it wil find app_name since we write CREATE_USER_URL = reverse('user:create')
app_name = 'user'
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('login/', views.CreateTokenView.as_view(), name='login'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
