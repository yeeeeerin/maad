from django.contrib import admin
from .models import URLData, Project, Folder, TextData
# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
	list_display = ('name','publish_date')

class FolderAdmin(admin.ModelAdmin):
	list_display = ('title','created_date','proj')

class URLDataAdmin(admin.ModelAdmin):
	list_display = ('title','link','tag','folder')

admin.site.register(URLData,URLDataAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Folder, FolderAdmin)
admin.site.register(TextData)


