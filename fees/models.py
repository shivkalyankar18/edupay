from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal
from users.models import CustomUser
from courses.models import Course


class Fee(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('partially_paid', 'Partially Paid'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('waived', 'Waived'),
    )

    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='fees')
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    late_fee_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=5)
    late_fee_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fees_fee'
        ordering = ['-due_date']

    def __str__(self):
        return f"{self.student.username} - {self.course.course_code}"

    def get_remaining(self):
        return self.amount - self.amount_paid

    def is_overdue(self):
        return timezone.now().date() > self.due_date and self.status != 'paid'

    def update_status(self):
        remaining = self.get_remaining()
        if remaining <= 0:
            self.status = 'paid'
        elif self.amount_paid > 0:
            self.status = 'partially_paid'
        elif self.is_overdue():
            self.status = 'overdue'
        else:
            self.status = 'pending'
        self.save()