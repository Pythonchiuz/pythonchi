from django.shortcuts import redirect, render
from .forms import SignupForm
from django.contrib.auth import login, logout
from django.views import generic
from .models import Student, Group, Course, Modul, Homework, Lesson, Chat, Book, Certificate, Task, ModulStatus
from django.contrib.auth.decorators import login_required

def home(request):
    courses = Course.objects.all()
    return render(request, 'project/index.html', {"courses": courses})

def signUp(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            signup = form.save()
            login(request, signup, backend='django.contrib.auth.backends.ModelBackend')
        return redirect(to='home')

    else:
        form = SignupForm()
    return render(request, 'project/signup.html', {"form": form})

def logOut(request, pk):
    student = Student.objects.get(pk=pk)
    if student is not None:
        logout(request)
        return redirect('home')
    return render(request, "layout/nav.html", {"student": student})


class logInModelView(generic.View):
    template_name = 'project/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        user = Student.objects.filter(username=username, last_name=last_name, password=password).first()

        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
        else:
            return redirect('signup')


def profile(request, student_id):
    student = Student.objects.get(student_id=student_id)
    courses = Course.objects.all()
    groups = Group.objects.all().filter(student=student)
    return render(request, 'project/my-course.html', {"student": student, "groups": groups, "courses": courses})


def allCourses(request, student_id):
    courses = Course.objects.all()
    student = Student.objects.get(student_id=student_id)
    return render(request, 'project/all-course.html', {"courses": courses, "student": student})

def settings(request, student_id):
    student = Student.objects.get(student_id=student_id)
    return render(request, "project/users-profile.html", {"student": student})

def chat(request, student_id):
    chats = Chat.objects.all()
    student = Student.objects.get(student_id=student_id)
    comments = Task.objects.all().filter(student=student)
    return render(request, "project/chat.html", {"chats": chats, "student": student, "comments": comments})

def books(request, student_id):
    books = Book.objects.all()
    student = Student.objects.get(student_id=student_id)
    return render(request, "project/book.html", {"books": books, "student": student})

def certificate(request, student_id):
    student = Student.objects.get(student_id=student_id)
    certificate = Certificate.objects.filter(student=student).first()
    return render(request, "project/certificate.html", {"certificate": certificate, "student": student})

def moduls(request, student_id, name):
    student = Student.objects.get(student_id=student_id)
    group = Group.objects.get(name=name)
    status = ModulStatus.objects.all().filter(group=group)
    return render(request, "project/course-detail.html", {"moduls": moduls, "group": group, "student": student, "status": status})

def lesson(request, student_id, pk, name):
    student = Student.objects.get(student_id=student_id)
    group = Group.objects.get(pk=pk)
    modul = Modul.objects.get(name=name)
    lesson = Lesson.objects.all().filter(group__lesson__modul=modul)
    homeworks = Homework.objects.all().filter(modul__name=modul.name)
    moduls = ModulStatus.objects.all().filter(group=group)
    return render(request, "project/lesson.html", {"modul": modul, "group":group, "lesson": lesson, "student": student, "homeworks": homeworks, "moduls": moduls})

def homeworks(request, student_id, pk, name):
    student = Student.objects.get(student_id=student_id)
    group = Group.objects.get(pk=pk)
    modul = Modul.objects.get(name=name)
    lesson = Lesson.objects.all().filter(group__lesson__modul=modul)
    homeworks = Homework.objects.all().filter(modul__name=modul.name)
    moduls = ModulStatus.objects.all().filter(group=group)
    return render(request, "project/homeworks.html",
                  {"modul": modul, "group": group, "lesson": lesson, "student": student, "homeworks": homeworks,
                   "moduls": moduls})

def homework(request, student_id, pk, name, title):
    # Получение данных из базы
    student = Student.objects.get(student_id=student_id)
    group = Group.objects.get(pk=pk)
    modul = Modul.objects.get(name=name)
    homework = Homework.objects.get(title=title)
    homeworks = Homework.objects.all().filter(modul__name=modul.name)
    moduls = ModulStatus.objects.all().filter(group=group)
    lesson = Lesson.objects.all().filter(modul__name=modul.name)

    # Проверка, отправлено ли задание
    task_is_submitted = Task.objects.filter(student=student, group=group, modul=modul, hw=homework).exists()

    # Если задание уже отправлено, показываем его
    if task_is_submitted:
        task = Task.objects.get(student=student, group=group, modul=modul, hw=homework)
        return render(request, "project/homework.html", {
            "modul": modul,
            "lesson": lesson,
            "group": group,
            "student": student,
            "homework": homework,
            "homeworks": homeworks,
            "task": task,
            "moduls": moduls,
            "task_is_submitted": task_is_submitted
        })

    # Если задание не отправлено, обрабатываем форму
    if request.method == "POST":
        homework_text = request.POST.get('homework')

        # Создание новой задачи
        task = Task(student=student, group=group, modul=modul, hw=homework, homework=homework_text)
        task.save()

        return redirect('homework', student_id=student.student_id, pk=group.pk, name=modul.name, title=homework.title)

    # Отображаем страницу, если задание не отправлено
    return render(request, "project/homework.html", {
        "modul": modul,
        "group": group,
        "lesson": lesson,
        "student": student,
        "homework": homework,
        "homeworks": homeworks,
        "moduls": moduls,
        "task_is_submitted": task_is_submitted
    })


@login_required
def edit_profile(request, student_id):
    if request.POST:

        student = Student.objects.get(student_id=student_id)
        student.username = request.POST.get('username')
        student.last_name = request.POST.get('last_name')
        student.about = request.POST.get('about')
        student.address = request.POST.get('address')
        student.age = request.POST.get('age')
        student.edu_name = request.POST.get('edu_name')
        student.number = request.POST.get('number')
        student.telegram = request.POST.get('telegram')
        student.linkedin = request.POST.get('linkedin')
        student.github = request.POST.get('github')
        student.save()

        return redirect('settings', student_id=student_id)

    student = Student.objects.get(student_id=student_id)
    return render(request, 'project/users-profile.html', {'student': student})

