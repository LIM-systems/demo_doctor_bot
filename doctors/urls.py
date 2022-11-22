from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from doctors import settings

urlpatterns = [
    path('admin/', admin.site.urls),
]
