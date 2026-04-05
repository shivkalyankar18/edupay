from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import CustomUser, AuditLog
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .forms import CustomUserCreationForm, CustomUserChangeForm, StudentRegistrationForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            AuditLog.objects.create(
                user=user,
                action='login',
                entity_type='User',
                entity_id=user.id,
                description=f'User {username} logged in'
            )
            messages.success(request, f'Welcome, {user.get_full_name()}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'users/login.html')


def logout_view(request):
    user = request.user
    AuditLog.objects.create(
        user=user,
        action='logout',
        entity_type='User',
        entity_id=user.id,
        description=f'User {user.username} logged out'
    )
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')


def home_view(request):
    return render(request, 'home.html')


@login_required(login_url='login')
def dashboard_view(request):
    """
    Route to correct dashboard based on user role
    """
    user = request.user

    # Admin Dashboard
    if user.is_admin():
        from django.db.models import Sum
        from users.models import CustomUser
        from courses.models import Course
        from fees.models import Fee
        from payments.models import Payment

        context = {
            'total_users': CustomUser.objects.count(),
            'total_courses': Course.objects.count(),
            'total_fees': Fee.objects.aggregate(Sum('amount'))['amount__sum'] or 0,
            'total_collected': Payment.objects.filter(status='confirmed').aggregate(Sum('amount'))['amount__sum'] or 0,
        }
        return render(request, 'dashboard_admin.html', context)

    # Accountant Dashboard
    elif user.is_accountant():
        from django.db.models import Sum
        from fees.models import Fee
        from payments.models import Payment

        all_fees = Fee.objects.all()
        context = {
            'total_fees': all_fees.aggregate(Sum('amount'))['amount__sum'] or 0,
            'total_collected': Payment.objects.filter(status='confirmed').aggregate(Sum('amount'))['amount__sum'] or 0,
            'pending_amount': all_fees.filter(status='pending').aggregate(Sum('amount'))['amount__sum'] or 0,
        }
        return render(request, 'dashboard_accountant.html', context)

    # Student Dashboard
    elif user.is_student():
        from django.db.models import Sum
        from fees.models import Fee

        student_fees = Fee.objects.filter(student=user)
        total_fees = student_fees.aggregate(Sum('amount'))['amount__sum'] or 0
        total_paid = student_fees.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

        context = {
            'total_fees': total_fees,
            'total_paid': total_paid,
            'total_remaining': total_fees - total_paid,
            'recent_fees': student_fees[:5],
        }
        return render(request, 'dashboard_student.html', context)

    # Default dashboard for other roles
    return render(request, 'dashboard.html')

def is_admin(user):
    return user.is_authenticated and user.is_admin()


@login_required(login_url='login')
@user_passes_test(is_admin)
def user_list_view(request):
    search = request.GET.get('search', '')
    role = request.GET.get('role', '')

    users = CustomUser.objects.all()

    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(email__icontains=search)
        )

    if role:
        users = users.filter(role=role)

    paginator = Paginator(users, 10)
    page = request.GET.get('page')
    users = paginator.get_page(page)

    return render(request, 'users/user_list.html', {'users': users, 'search': search})


@login_required(login_url='login')
@user_passes_test(is_admin)
def user_create_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.get_full_name()} created!')
            return redirect('user-list')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/user_form.html', {'form': form, 'title': 'Create User'})


@login_required(login_url='login')
@user_passes_test(is_admin)
def user_edit_view(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated!')
            return redirect('user-list')
    else:
        form = CustomUserChangeForm(instance=user)

    return render(request, 'users/user_form.html', {'form': form, 'title': 'Edit User'})


@login_required(login_url='login')
def profile_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'users/profile.html', {'form': form})


def register_view(request):
    """
    Public registration view for students
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please login with your credentials.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = StudentRegistrationForm()

    return render(request, 'users/register.html', {'form': form})