from django.db import models
from django.core.validators import MinValueValidator
from users.models import CustomUser


class Course(models.Model):
    SEMESTER_CHOICES = (
        ('1', 'Semester 1'),
        ('2', 'Semester 2'),
        ('3', 'Semester 3'),
        ('4', 'Semester 4'),
        ('5', 'Semester 5'),
        ('6', 'Semester 6'),
        ('7', 'Semester 7'),
        ('8', 'Semester 8'),
    )

    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    department = models.CharField(max_length=100)
    semester = models.CharField(max_length=2, choices=SEMESTER_CHOICES)
    credits = models.IntegerField(default=3, validators=[MinValueValidator(1)])
    base_fee = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    lab_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    library_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    activity_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'courses_course'
        ordering = ['department', 'semester']

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"

    def get_total_fee(self):
        return self.base_fee + self.lab_fee + self.library_fee + self.activity_fee


class StudentCourse(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='courses')
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'courses_studentcourse'
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} - {self.course.course_code}"