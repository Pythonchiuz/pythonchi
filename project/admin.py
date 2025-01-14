from django.contrib import admin
from .models import *
from django.utils.html import format_html


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = ("student", "code", "procent", "count")
    search_fields = ("count", "procent",)
    list_filter = ("count", "procent",)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("username", "last_name", "number", "address", "age", "edu_name", "about", "telegram_chat_id", "telegram", "linkedin", "github", "password")
    search_fields = ("username", "last_name", "number", "age",)
    list_filter = ("age", "edu_name",)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "count_lesson", "course_price", "course_start", "discount_status", "discount_price")
    list_filter = ("name", "count_lesson", "discount_status",)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "course")
    search_fields = ("name",)
    list_filter = ("course",)

@admin.register(Modul)
class ModulAdmin(admin.ModelAdmin):
    list_display = ("name", "course")
    search_fields = ("name",)
    list_filter = ("course",)

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ("group", "modul", "title", "text")
    search_fields = ("title", "text",)
    list_filter = ("group", "modul",)

@admin.register(ModulStatus)
class ModulStatusAdmin(admin.ModelAdmin):
    list_display = ("group", "modul", "status")
    list_filter = ("group", "modul", "status",)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("group", "modul", "teory_text", "code", "source_code", "video_link")
    list_filter = ("group", "modul",)

    def example(self):
        return format_html('TYPE : %s<br> RATE : %s<br> FAMILY %s' % (
            self.type, self.rate, self.family))



@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("homework", "comment_text", "homework_status", "comment_status", "student", "group", "modul", "hw")
    list_filter = ("student", "group", "modul", "hw", "homework_status", "comment_status",)

@admin.register(Book)
class BooksAdmin(admin.ModelAdmin):
    list_display = ("image", "link")

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("group", "title", "text", "lesson_link", "status")
    list_filter = ("group", "status",)

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("student", "image", "status")
    list_filter = ("student", "status",)