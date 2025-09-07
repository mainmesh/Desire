from django.contrib import admin
from django.urls import path, include
admin.site.site_header="Desire"
admin.site.site_title ="Admin Desire"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls'))
]
