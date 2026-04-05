from django.contrib import admin
from .models import Fee

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'amount', 'status', 'due_date')
    list_filter = ('status', 'due_date')
    search_fields = ('student__username', 'course__course_code')