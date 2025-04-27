# dj_ekzamen
1. Django-ның негізгі компоненттері. 
models - базамен жұмыс істейтін бөлік, таблицалар
views - қолданушының сұранысына жауап беретін логика, сұранысты алып html немесе json түрінде қайтарады
templates - html шығаратын бөлім, деректерді әдемі жеткізу үшін қолданылады
urls - сұраныстарды views қа бағыттайды
admin - дайын админ панель ұсынады
forms - деректерді қолданушылардан жинауға арналған компонент, валидация, сериализация жүреді
middleware - сервер мен қолданушы сұранысын/жауабы арасындағы қосымша өңдеу жұмыстары жүретін бөлім
settings - жоба конфигурациясы
static files - ccs, javascript, суреттер сияқты ресурстар
django orm - sql запрос жазбай ақ, python обьектілері арқылы дерекқормен дүмыс істеуге мүмкіндік береді

5. Django-да URL маршрутизациясы, мысал келтіріп түсіндіріңіз. 
django проектысында әр сұраныс (/home, /about) белгілі бір view функциясына немесе класына жіберіледі, мұны жасау үшін urls қолданылады
мысал:
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about')
]

6. Django ORM дегеніміз не және оның негізгі функциялары.
django ORM(object-realtional-mapping) - бұл django-да базамен (postgresql, mysql, sqllite) Python кодымен жұмыс істеуге мүмкіндік береді.
негізгі функциялары
CRUD - Create, Read, Update, Delete

7. Жобаның құрылуы. Django-да миграция (migration) дегеніміз не, 
орындалу тәртібі. 
проект құру үшін - django-admin startproject projectname
миграция файлын жасау - python manage.py makemigrations
миграцияны базаға жазу - python manage.py migrate

8. Django-да админ панелі, атқаратын функциялары, қалыптастырылуы.
django admin panel - бұл дайын, автоматты түрде жасалатын веб-интерфейс, ол арқылы сайттың дерекқорын басқара аласыз
admin жасау - python manage.py createsuperuser
admin панель қосу:
INSTALLED APPS = [
    ....,
    'django.contrib.admin',
]
модельді админ панельде көрсету:
from django.contrib import admin 
from .models import Student

admin.site.register(Student)
әдемілеу:
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'age') - админ панельде не көрсетілуі керек
    search_fields = ('name',) - іздеу мүмкіндігі
    list_filter = ('age',) - фильтрлеу мүмкіндігі

admin.site.register(Student, StudentAdmin)

9. Django-да формалар (forms) жұмыс істеу принципін, жоба ішінде 
құрылымдық байланысты сипаттаңыз.
django forms - бұл қолданушылардан мәлімет жинауға және оны тексеруге арналған қуатты механизм, яғни валидация - қолданушыдан дұрыс мәліметтер келсе базаға сақтайды
Мысал:
models.py
from django.db import models

class Student(models.Model):
    name = models.CharField(max_lenght=100)
    email = models.EmailField()
    age = models.IntegerField()

forms.py
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'age']

10. Django-да аутентификацияның (authentication) жүзеге асырылу 
процесі.
authentication - login,register,logout
мысал:
views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import User

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Пароль или логин неправильный'})
    return render(request, 'login.html')

def user_register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            return render(request, 'register.html', {'error': 'Пароли не совпадают'})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'такой пользователь уже существует'})

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')

    return render(request, 'register.html')

def user_logout(request):
    logout(request)
    return redirect('login')

11. Django-да конфигурация файлдары (settings.py) параметрлерін 
сипаттаңыз. 
DEBUG=True - True болса қате туралы барлық ақпаратты береді
SECRET_KEY='dfdfdfdfd' - Проект қауіпсіздігі үшін
ALLOWED_HOSTS = ['127.0.0.1', 'localhost'] - рұқсат берілген хосттар
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    .....,
] - проектке қосылған қосымашалар
DATABASES = [
    'default': {
        'ENGINE': 'django.db.backends.sqllite3',
        'NAME': BASE_DIR / 'db.sqllite3',
    }
] - базаға қосылу
STATIC_URL = '/static/' - статикалық файлдар
MEDIA_URL = '/media/' - суреттер
LANGUAGE_CODE = 'kk' - тіл
TIME_ZONE = 'Asia/Almaty' - уақыт

13. Django-да формаларды валидациялау (validation) қалай жүзеге 
асырылады? 
forms.py
from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)

views.py
from django.shortcuts import render
from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            return render(request, 'succes.html')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

is_valid және cleaned_data

14. Django-да модельдер арасындағы байланыстардың (relationship) 
орнатылуы. 
OneToOneField:
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

OneToManyField:
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

ManyToManyField:
class Student(models.Model):
    name = models.CharField(max_length=120)

class Course(models.Model):
    student = models.ManyToManyField(Student)

15. Django-да URL конфигурациясында include() функциясының рөлі 
қандай, мысал келтіріп түсіндіріңіз. 
include() - django конфигурациясында басқа app url-ын проектің басты url-на қосу
urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    ....
]

18. Django ORM-да деректерді сұрауды (query) жүзеге асыру жолдары, 
мысал келтіріп түсіндіріңіз. 
all() - барлық жазбаны алады
filter() - белгілі бір шартпен деректі алады
exclude() - белгілі бір шартпен деректерді алып тастайды
get() - нақты бір обьектіні қайтарады
order_by() - деректерді сұрыптайды
values() - деректерді сөздік ретінде қайтарады
count() - неше жазба бар екенін айтады

20. Django жобасының базалық конфигурация файлында (settings.py) 
«STATIC_URL» және «STATIC_URL» айырмашылықтары, конфигурациялау. 
«TIME_ZONE» параметрінің қажеттілігі, конфигурациялау. «SECRET_KEY» 
параметрі, қауіпсіз сақтау жолдары. 
STATIC_URL = '/static/' - статикалық файлдарға сілтеме
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
] - static папкадан файлдар алынады

21. Django-да шаблон тегтері (template tags) мен фильтрлер (filters).
тегтер:
{% for %} - цикл жасау {% for product in products %} {{ product.name }} {% endfor %}
{% if %} - шарт тексеру {% if user.is_authenticated %} Қош келдіңіз {% endif %}
{% url %} - url генерациялау {% url 'home' %}
{% block %} - блок анықтау (extend үшін) {% block content %}{% endblock %}
{% extends %} - басқа шаблонды кеңейту {% extends 'base.html' %}
{% include %} - басқа файл қосу {% include 'navbar.html' %}

фильтрлер:
lower - барлық әріптерді кішірейту 
upper - барлық әріптерді үлкейту
length - ұзындығын есептеу
date - датаны форматтау
truncatechars - мәтінді қысқарту
default - бос болса басқа мән беру

22. Django-да формаларды динамикалық түрде жасалуы.
from django import forms
from .models import Category, Product

class ProductChoiceForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.obejects.all(), label='Категорияны таңдаңыз')

    def __init__(self, *args, **kwargs):
        selected_category = kwargs.pop('selected_category', None)
        super(ProductChoiceForm, self).__init__(*args, **kwargs)

        if selected_category:
            self.fields['product'] = forms.ModelChoiceField(
                queryset=Product.objects.filter(category=selected_category),
                label="Өнімді таңдаңыз"
            )

24. Джанго жобасының құрылымы. Жоба мен қосымша құру, мысал 
келтіріңіз. 
Жоба құру: python manage.py startapp app

25. Django-да API-лерді құру үшін қажетті кітапханаларды сипаттаңыз. 
djangorestframework, django-cors-headers, drf-yasg, jwt, djangorestframework-simplejwt

26. Django-да шаблонды мұрагерліктің (template inheritance) асырылу 
жолы, тізбектеп мысалдар түрінде түсіндіріңіз. 
{% extends %} қолданылады
мысал
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}My Website{% endblock %}</title>
</head>
<body>
    <header>
        <h1>Басты бет</h1>
        <nav>
            <a href="/">Үйге</a> |
            <a href="/about/">Біз туралы</a> |
            <a href="/contact/">Байланыс</a>
        </nav>
    </header>

    <main>
        {% block content %}
        <!-- Әр беттің мазмұны осында келеді -->
        {% endblock %}
    </main>

    <footer>
        <p>© 2025 Менің сайтым</p>
    </footer>
</body>
</html>

30. Django жобасының базалық конфигурация файлында (settings.py) 
«DATABASES», «INSTALLED_APPS», «MIDDLEWARE», «TEMPLATES»  
параметрлерінің қажеттілктері, құрамдарындағы элементтерді сипаттап 
түсіндіріңіз.  
Middleware - HTTP сұраныс/жауап циклында әр түрлі өңдеулер жасау үшін (қауіпсіздік, сессия сақтау, куки өңдеу).
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',     # Қауіпсіздік
    'django.contrib.sessions.middleware.SessionMiddleware', # Сессия
    'django.middleware.common.CommonMiddleware',          # Ортақ баптаулар
    'django.middleware.csrf.CsrfViewMiddleware',          # CSRF қорғау
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Аутентификация
    'django.contrib.messages.middleware.MessageMiddleware',   # Хабарламалар
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Клик-ұрлау қорғанысы
]
templates - Django-ға HTML шаблондарын қай жерден іздеу керек екенін және шаблон жүйесі қалай жұмыс істейтінін көрсету.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Django шаблон механизмі
        'DIRS': [BASE_DIR / 'templates'],  # Жеке templates папка қосу
        'APP_DIRS': True,                  # Әр қосымшадағы templates/ папкаларын сканерлеу
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
