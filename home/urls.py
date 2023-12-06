from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('signIn/',sign_in,name='sign_in'),
    path('signOut/',sign_out,name='sign_out'),
    path('signUp/',sign_up,name='sign_up'),
    path('calendar/',calendar_view,name='calendar_view'),
    
]
