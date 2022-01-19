"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from accounts.views import UserViewSet
from user_profile.views import ProfileViewSet, DeliveryAddressViewSet
from vendor.views import VendorViewSet
from stores.views import CategoryViewSet, ProductViewSet, ImageViewSet, SpecificationViewSet
from address.views import StateViewSet, DistrictViewSet, PINViewSet, VillageOrTownViewSet
from orders.views import OrderViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'delivery_addresses', DeliveryAddressViewSet)
router.register(r'vendor', VendorViewSet)
router.register(r'store/category', CategoryViewSet)
router.register(r'store/products', ProductViewSet)
router.register(r'store/images', ImageViewSet)
router.register(r'store/specification', SpecificationViewSet)
router.register(r'address/states', StateViewSet )
router.register(r'address/districts', DistrictViewSet)
router.register(r'address/PINs', PINViewSet)
router.register(r'address/villageOrTowns', VillageOrTownViewSet)
router.register(r'orders', OrderViewSet)



urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),

    # simple JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
