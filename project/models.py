from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, User


class Student(AbstractUser):
    student_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    last_name = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    address = models.CharField(max_length=2555, null=True, blank=True)
    age = models.CharField(max_length=255, null=True, blank=True)
    edu_name = models.CharField(max_length=2555, null=True, blank=True)
    about = models.CharField(max_length=25555, null=True, blank=True)
    telegram = models.CharField(max_length=2555, null=True, blank=True)
    linkedin = models.CharField(max_length=2555, null=True, blank=True)
    github = models.CharField(max_length=2555, null=True, blank=True)
    telegram_chat_id = models.CharField(max_length=255, null=True, blank=True)
    IS_ACTIVE = 'IS_ACTIVE'
    IN_ACTIVE = 'IN_ACTIVE'
    STATUS_CHOICES = [
        (IS_ACTIVE, "is_active"),
        (IN_ACTIVE, "in_active"),
    ]
    status = models.CharField(max_length=25, default=IN_ACTIVE, choices=STATUS_CHOICES)

    def __str__(self):
        return f'{self.last_name} {self.username}'

class Promocode(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, null=True, blank=True)
    procent = models.CharField(max_length=255, null=True, blank=True)
    count = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.code

class Course(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=25555, null=True, blank=True)
    count_lesson = models.CharField(max_length=255, null=True, blank=True)
    course_price = models.CharField(max_length=255, null=True, blank=True)
    course_start = models.CharField(max_length=255, null=True, blank=True)
    IS_ACTIVE = 'IS_ACTIVE'
    IN_ACTIVE = 'IN_ACTIVE'
    STATUS_CHOICES = [
        (IS_ACTIVE, "is_active"),
        (IN_ACTIVE, "in_active"),
    ]
    discount_status = models.CharField(max_length=25, default=IN_ACTIVE, choices=STATUS_CHOICES)
    discount_price = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=2555, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ManyToManyField(Student)
    IS_ACTIVE = 'IS_ACTIVE'
    IN_ACTIVE = 'IN_ACTIVE'
    STATUS_CHOICES = [
        (IS_ACTIVE, "is_active"),
        (IN_ACTIVE, "in_active"),
    ]
    status = models.CharField(max_length=25, default=IN_ACTIVE, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name

class Modul(models.Model):
    name = models.CharField(max_length=25555, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    modul = models.ForeignKey(Modul, on_delete=models.CASCADE)
    teory_text = models.TextField(max_length=25555, null=True, blank=True)
    code = models.TextField(max_length=25555, null=True, blank=True)
    source_code = models.CharField(max_length=2555, null=True, blank=True)
    video_link = models.CharField(max_length=2555, null=True, blank=True)

class Homework(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    modul = models.ForeignKey(Modul, on_delete=models.CASCADE)
    title = models.CharField(max_length=2555, null=True, blank=True)
    text = models.CharField(max_length=2555, null=True, blank=True)

class ModulStatus(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    modul = models.ForeignKey(Modul, on_delete=models.CASCADE)
    IS_ACTIVE = 'IS_ACTIVE'
    IN_ACTIVE = 'IN_ACTIVE'
    STATUS_CHOICES = [
        (IS_ACTIVE, "is_active"),
        (IN_ACTIVE, "in_active"),
    ]
    status = models.CharField(max_length=25, choices=STATUS_CHOICES)

class Chat(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    title = models.CharField(max_length=25555, null=True, blank=True)
    lesson_link = models.CharField(max_length=25555, null=True, blank=True)
    text = models.CharField(max_length=25555, null=True, blank=True)
    IS_ACTIVE = 'IS_ACTIVE'
    IN_ACTIVE = 'IN_ACTIVE'
    STATUS_CHOICES = [
        (IS_ACTIVE, "is_active"),
        (IN_ACTIVE, "in_active"),
    ]
    status = models.CharField(max_length=25, default=IN_ACTIVE, choices=STATUS_CHOICES)

class Book(models.Model):
    image = models.ImageField(upload_to='images/')
    link = models.CharField(max_length=25555, null=True, blank=True)

class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    image = models.CharField(max_length=25555, null=True, blank=True)
    IS_ACTIVE = 'IS_ACTIVE'
    IN_ACTIVE = 'IN_ACTIVE'
    STATUS_CHOICES = [
        (IS_ACTIVE, "is_active"),
        (IN_ACTIVE, "in_active"),
    ]
    status = models.CharField(max_length=25, default=IN_ACTIVE, choices=STATUS_CHOICES)

class Task(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    modul = models.ForeignKey(Modul, on_delete=models.CASCADE)
    hw = models.ForeignKey(Homework, on_delete=models.CASCADE)
    homework = models.CharField(max_length=25555, null=True, blank=True)
    comment_text = models.CharField(max_length=2555, null=True, blank=True)
    IS_ACTIVE = 'IS_ACTIVE'
    IN_ACTIVE = 'IN_ACTIVE'
    STATUS_CHOICES = [
        (IS_ACTIVE, "is_active"),
        (IN_ACTIVE, "in_active"),
    ]
    comment_status = models.CharField(max_length=25, default=IN_ACTIVE, choices=STATUS_CHOICES)
    homework_status = models.CharField(max_length=25, default=IN_ACTIVE, choices=STATUS_CHOICES)