from django.urls import path
from .views import user_login, dashboard, user_logout

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
]