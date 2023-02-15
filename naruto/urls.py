from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.viewsets import CharacterViewSet, CategoryViewSet


router = routers.DefaultRouter()
router.register('characters', CharacterViewSet, basename='characters')
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/<str:language>', include(router.urls)),
]
