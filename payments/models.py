from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from users.models import CustomUser
from fees.models import Fee


class Payment(models.Model):
    METHOD_CHOICES = (
        ('online', 'Online'),
        ('cheque', 'Cheque'),
        ('cash', 'Cash'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('failed', 'Failed'),
    )

    fee = models.ForeignKey(Fee, on_delete=models.CASCADE, related_name='payments')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    receipt_generated = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payments_payment'
        ordering = ['-payment_date']

    def __str__(self):
        return f"Payment {self.transaction_id}"