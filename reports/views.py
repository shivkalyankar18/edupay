from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count
from fees.models import Fee
from payments.models import Payment


def is_admin_or_accountant(user):
    return user.is_authenticated and (user.is_admin() or user.is_accountant())


@login_required(login_url='login')
@user_passes_test(is_admin_or_accountant)
def payment_collection_report_view(request):
    payments = Payment.objects.filter(status='confirmed').select_related('student', 'fee__course')

    total_collected = payments.aggregate(Sum('amount'))['amount__sum'] or 0
    total_transactions = payments.count()

    return render(request, 'reports/payment_collection.html', {
        'total_collected': total_collected,
        'total_transactions': total_transactions,
        'payments': payments[:50]
    })


@login_required(login_url='login')
@user_passes_test(is_admin_or_accountant)
def fee_status_report_view(request):
    fees = Fee.objects.select_related('student', 'course')

    by_status = fees.values('status').annotate(
        total=Sum('amount'),
        count=Count('id')
    )

    total_fee = fees.aggregate(Sum('amount'))['amount__sum'] or 0
    total_paid = fees.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

    return render(request, 'reports/fee_status.html', {
        'total_fee': total_fee,
        'total_paid': total_paid,
        'by_status': by_status,
        'fees': fees[:50]
    })


@login_required(login_url='login')
@user_passes_test(is_admin_or_accountant)
def overdue_report_view(request):
    overdue_fees = Fee.objects.filter(status='overdue').select_related('student', 'course')

    total_overdue = overdue_fees.aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request, 'reports/overdue.html', {
        'fees': overdue_fees,
        'total_overdue': total_overdue
    })