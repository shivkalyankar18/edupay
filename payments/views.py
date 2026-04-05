from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Payment
from .forms import PaymentForm
from fees.models import Fee
import uuid


@login_required(login_url='login')
def payment_create_view(request, fee_id):
    from notifications.models import Notification

    fee = get_object_or_404(Fee, pk=fee_id)

    # Check if student owns this fee
    if fee.student != request.user:
        messages.error(request, 'Access denied')
        return redirect('dashboard')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.fee = fee
            payment.student = request.user
            payment.status = 'confirmed'
            payment.save()

            # Update fee amount paid
            fee.amount_paid += payment.amount
            fee.update_status()
            fee.save()

            # CREATE NOTIFICATION FOR STUDENT
            Notification.objects.create(
                recipient=request.user,
                notif_type='payment_received',
                title='Payment Confirmed',
                message=f'Your payment of ₹{payment.amount} for {fee.course.course_code} has been confirmed. Transaction ID: {payment.transaction_id}'
            )

            messages.success(request, 'Payment recorded successfully!')
            return redirect('fee-detail', pk=fee.pk)
    else:
        form = PaymentForm(initial={'amount': fee.get_remaining()})

    return render(request, 'payments/payment_form.html', {'form': form, 'fee': fee})

@login_required(login_url='login')
def payment_history_view(request):
    payments = Payment.objects.filter(student=request.user).select_related('fee')
    return render(request, 'payments/payment_history.html', {'payments': payments})