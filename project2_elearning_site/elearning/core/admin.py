from django.contrib import admin
from .models import *
# Register your models here.

class TagAdmin(admin.TabularInline):
    model = Tag

class LearningAdmin(admin.TabularInline):
    model = Learning


class PrerequisiteAdmin(admin.TabularInline):
    model = Prerequisite

class ViedoAdmin(admin.StackedInline):
    model = Video


class CoursesAdmin(admin.ModelAdmin):
    inlines = [TagAdmin, LearningAdmin, PrerequisiteAdmin, ViedoAdmin]


admin.site.register(Courses, CoursesAdmin)
admin.site.register(Video)
admin.site.register(Payment)
admin.site.register(UserCourse)
