from django.contrib import admin
from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'githubdetails', GithubDetailsViewSet)
router.register(r'appdetails', AppDetailsViewSet)
router.register(r'appplans', AppPlansViewSet)
router.register(r'databasedetails', DatabaseDetailsViewSet)
router.register(r'dbplans', DbPlansViewSet)
router.register(r'envvariables', EnvVariablesViewSet)

urlpatterns = [
    path("register/",RegistrationView.as_view(),name="register"),
    path("login/",LoginAPIView.as_view(),name="login"),
    path("refresh/",CustomTokenRefreshView.as_view(),name="refresh"),
    path("logout/",LogoutView.as_view(),name="logout"),
    path('', include(router.urls)),
]



