from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from api.viewsets import CharacterViewSet, CategoryViewSet


router = routers.DefaultRouter()
router.register(r'(?P<language>[a-zA-Z]+)/characters', CharacterViewSet, basename='characters')
router.register('fr/categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    re_path(r'^api/(?P<version>(v1))/', include(router.urls)),
]
