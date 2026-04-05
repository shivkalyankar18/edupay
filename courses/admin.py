from django.contrib import admin
from .models import Course, StudentCourse

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name', 'department', 'semester', 'base_fee')
    list_filter = ('department', 'semester')
    search_fields = ('course_code', 'course_name')
    fieldsets = (
        ('Basic Info', {'fields': ('course_code', 'course_name', 'description', 'department', 'semester')}),
        ('Fees', {'fields': ('base_fee', 'lab_fee', 'library_fee', 'activity_fee')}),
    )


@admin.register(StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date')
    list_filter = ('enrollment_date',)
    search_fields = ('student__username', 'course__course_code')