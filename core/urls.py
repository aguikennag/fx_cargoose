from .views import LoginRedirect
from django.urls import path,include

from . import blog

urlpatterns = [
    path('login-redirect',LoginRedirect.as_view(),name = 'login-redirect'),


    #BLOG
    path("blog/",blog.BlogList.as_view(),name='blog-list'),
    path("blog/<slug:slug>/",blog.BlogDetail.as_view(),name='blog-detail')
]