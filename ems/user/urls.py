from django.urls import path
from user.views import *

urlpatterns = [
    path('dashboard/', dashboard, name = 'dashboard'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path("logout/", logout_request, name="logout"),
    path('add/',add_expense.as_view(),name='add'),
    path('calender/',calender_request,name="calender"),
    path('profile/',profile,name="profile"),
    path('safe/',safe,name="safe"),
    path('analyse/',analyse,name="analyse"),
    # path('merchant/',merchant,name="merchant"),
    path('about/',about,name="about"),
    path('category/',category,name="category"),
    path('template/',template,name="template"),
    path('exp/',exp,name="exp"),
    # path('sendmail/',sendMail,name='sendmail'),
    path('success/',success,name='success'),
    path('forget/',forget,name='forget'),
    
    
    
    
    ]