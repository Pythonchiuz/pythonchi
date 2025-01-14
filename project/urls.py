from django.urls import path
from .views import home, signUp, logInModelView, profile, edit_profile, logOut, allCourses, chat, certificate, books, moduls, lesson, homework, homeworks

urlpatterns = [
    path('', home, name="home"),
    path('signup/', signUp, name="signup"),
    path('login/', logInModelView.as_view(), name="login"),
    path('profile/<uuid:student_id>/', profile, name='profile'),
    path('profile/<uuid:student_id>/settings', edit_profile, name="settings"),
    path('profile/<uuid:student_id>/logout', logOut, name="logout"),
    path('profile/<uuid:student_id>/all-courses', allCourses, name="all-courses"),
    path('profile/<uuid:student_id>/chat', chat, name="chat"),
    path('profile/<uuid:student_id>/books', books, name="books"),
    path('profile/<uuid:student_id>/certificate', certificate, name="certificate"),
    path('profile/<uuid:student_id>/<str:name>', moduls, name="moduls"),
    path('profile/<uuid:student_id>/<int:pk>/lesson-<str:name>', lesson, name="lesson"),
    path('profile/<uuid:student_id>/<int:pk>/lesson-<str:name>/homeworks', homeworks, name="homeworks"),
    path('profile/<uuid:student_id>/<int:pk>/lesson-<str:name>/homework-<str:title>', homework, name="homework"),
]
