from django.urls import include, path
from rest_framework.routers import DefaultRouter
from accounts import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
]



