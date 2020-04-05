from django.contrib import admin
from .models import Question, Answer, Commend, Profile

# Register your models here.
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Commend)
admin.site.register(Profile)