from django.db import models
from users.models import CustomUser


class Notification(models.Model):
    TYPE_CHOICES = (
        ('fee_assigned', 'Fee Assigned'),
        ('payment_received', 'Payment Received'),
        ('payment_overdue', 'Payment Overdue'),
        ('other', 'Other'),
    )

    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    notif_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications_notification'
        ordering = ['-created_at']