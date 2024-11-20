from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImageViewSet, upload_image

router = DefaultRouter()
router.register(r'images', ImageViewSet)

urlpatterns = [
    path('upload/image/', upload_image, name='upload_image'),
    path('', include(router.urls)),
]