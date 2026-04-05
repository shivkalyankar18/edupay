from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Sum
from django.core.paginator import Paginator
from .models import Fee
from .forms import FeeForm
from payments.models import Payment


def is_admin_or_accountant(user):
    return user.is_authenticated and (user.is_admin() or user.is_accountant())


@login_required(login_url='login')
def student_fee_list_view(request):
    if not request.user.is_student():
        messages.error(request, 'Access denied')
        return redirect('dashboard')

    fees = Fee.objects.filter(student=request.user)
    total_fee = fees.aggregate(Sum('amount'))['amount__sum'] or 0
    total_paid = fees.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

    return render(request, 'fees/student_fee_list.html', {
        'fees': fees,
        'total_fee': total_fee,
        'total_paid': total_paid,
        'total_remaining': total_fee - total_paid
    })


@login_required(login_url='login')
@user_passes_test(is_admin_or_accountant)
def fee_list_view(request):
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')

    fees = Fee.objects.select_related('student', 'course')

    if search:
        fees = fees.filter(Q(student__username__icontains=search))

    if status:
        fees = fees.filter(status=status)

    paginator = Paginator(fees, 20)
    fees = paginator.get_page(request.GET.get('page'))

    return render(request, 'fees/fee_list.html', {'fees': fees})


@login_required(login_url='login')
@user_passes_test(is_admin_or_accountant)
def fee_create_view(request):
    if request.method == 'POST':
        form = FeeForm(request.POST)
        if form.is_valid():
            fee = form.save()

            # CREATE NOTIFICATION FOR STUDENT
            from notifications.models import Notification
            Notification.objects.create(
                recipient=fee.student,
                notif_type='fee_assigned',
                title='New Fee Assigned',
                message=f'A new fee of ₹{fee.amount} has been assigned for {fee.course.course_code} ({fee.course.course_name}). Due date: {fee.due_date.strftime("%d %b %Y")}'
            )

            messages.success(request, 'Fee created and notification sent!')
            return redirect('fee-list')
    else:
        form = FeeForm()

    return render(request, 'fees/fee_form.html', {'form': form})

@login_required(login_url='login')
def fee_detail_view(request, pk):
    """
    View fee details with remaining amount and payment history
    """
    fee = get_object_or_404(Fee, pk=pk)

    # Permission check
    if request.user.is_student() and fee.student != request.user:
        messages.error(request, 'Access denied')
        return redirect('dashboard')

    # Calculate remaining amount
    remaining = fee.get_remaining()

    # Get all payments for this fee
    payments = Payment.objects.filter(fee=fee)

    context = {
        'fee': fee,
        'remaining': remaining,
        'payments': payments,
    }

    return render(request, 'fees/fee_detail.html', context)