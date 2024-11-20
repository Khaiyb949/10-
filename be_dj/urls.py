from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('dj_app.urls')),
    path('', include('myappname.urls')),
    path('api/', include('myappname.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.TRUYEN_IMAGES_URL, document_root=settings.TRUYEN_IMAGES_ROOT)
