from  django.urls import path,include
from .views import Subscribe
from .accounts import Register,LoginRedirect
from .dashboard import Dashboard

from .settings import UpdatePassword, UpdateSetting



urlpatterns = [
    #ACCOUNT
    path('subscribe/',Subscribe.as_view(),name = 'subscribe'),
    path('register/',Register.as_view(),name = 'register'),



    #SETTINGS
    path('settings/',UpdateSetting.as_view(),name = 'setting'),
    path('settings/update-password/',UpdatePassword.as_view(),name = 'update-password'),

    #DASHBOARD
    path('dashboard/',Dashboard.as_view(),name = 'dashboard'),

    path('login-redirect/',LoginRedirect.as_view(),name="login-redirect"),


    #path('profile/',Profile.as_view(),name = 'register'),
    

]