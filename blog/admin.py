from django.contrib import admin
from .models import Blog, post_suggestion,BlogComment,Like
# Register your models here.
admin.site.register((post_suggestion,BlogComment,Like))

@admin.register(Blog)

class BlogAdmin(admin.ModelAdmin):
	class Media:
		js=('inject.js',)