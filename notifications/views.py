from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required(login_url='login')
def notification_list_view(request):
    notifications = Notification.objects.filter(recipient=request.user)
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})