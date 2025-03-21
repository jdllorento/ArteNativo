from django.urls import path
from .views import user_login, dashboard, user_logout, basic_register, full_register

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('register/basic/', basic_register, name='basic_register'),
    path('register/full/', full_register, name='full_register'),
]
