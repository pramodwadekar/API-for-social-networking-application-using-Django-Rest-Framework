# API-for-social-networking-application-using-Django-Rest-Framework

# installation steps for django rest frmework

1.create environment
  . python -m venv apis_env
2. activete envirnment
  . .\apis_env\Scripts\activate  
3. pip install django  djangorestframework

4. create project
    django-admin startproject myproject
   
6. In myproject.setting.py
 INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
]

 7. Create app
   .python manage.py startapp users  

8. setting.py
   .INSTALLED_APPS = [
   .....
    'users'
]
8. myorojects.urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rest_framework.urls')),
    path('', include('users.urls')),
]

9. now create users.urls.py
    . add urls
10. Now add models
11. users.admin.py code
    from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(User)
admin.site.register(FriendRequest)

13. python manage.py createsuperuser
14. serializer.py code
15. python manage.py migrate
16. python manage.py makemigrations
17. refered views.py, urls.py
    


