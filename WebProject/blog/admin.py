from django.contrib import admin
from .models import Question, Answer, Commend, Profile
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


# Register your models here.
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Commend)
admin.site.register(Profile)

