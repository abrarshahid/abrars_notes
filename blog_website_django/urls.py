from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Abrar's Notes Administration"
admin.site.site_title = "Abrar's Notes Admin Panel"
admin.site.index_title = "Welcome to Abrar's Notes Admin Panel"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("blog.urls")),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
