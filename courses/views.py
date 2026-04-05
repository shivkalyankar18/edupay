from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Course, StudentCourse
from .forms import CourseForm


def is_admin(user):
    return user.is_authenticated and user.is_admin()


@login_required(login_url='login')
@user_passes_test(is_admin)
def course_list_view(request):
    search = request.GET.get('search', '')
    dept = request.GET.get('department', '')

    courses = Course.objects.all()

    if search:
        courses = courses.filter(Q(course_code__icontains=search) | Q(course_name__icontains=search))

    if dept:
        courses = courses.filter(department=dept)

    paginator = Paginator(courses, 10)
    courses = paginator.get_page(request.GET.get('page'))

    return render(request, 'courses/course_list.html', {'courses': courses, 'search': search})


@login_required(login_url='login')
@user_passes_test(is_admin)
def course_create_view(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course created!')
            return redirect('course-list')
    else:
        form = CourseForm()

    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Create Course'})


@login_required(login_url='login')
@user_passes_test(is_admin)
def course_edit_view(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated!')
            return redirect('course-list')
    else:
        form = CourseForm(instance=course)

    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Edit Course'})


@login_required(login_url='login')
def course_detail_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course, 'total_fee': course.get_total_fee()})