from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'student', 'amount', 'payment_method', 'status')
    list_filter = ('status', 'payment_method')
    search_fields = ('transaction_id', 'student__username')