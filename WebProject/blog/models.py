import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from taggit.managers import TaggableManager
from django.db.models import Sum
from django.utils import timezone
from PIL import Image
from taggit.models import Tag


class CommendManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        # Забираем queryset с записями больше 0
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        # Забираем queryset с записями меньше 0
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        # Забираем суммарный рейтинг
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

class Commend(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )

    vote = models.SmallIntegerField(verbose_name= ("Голос"), choices=VOTES)
    user = models.ForeignKey(User, verbose_name= ("Пользователь"), on_delete= models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = CommendManager()

class Question(models.Model):
    tags = TaggableManager()
    title = models.CharField(max_length=200)
    text = models.TextField()
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    votes = GenericRelation(Commend, related_query_name='articles')
    pub_date = models.DateTimeField('дата публикации')

#    def add_tags(self):

    def answers_count(self):
        answers = {}
        for question in Question.objects.all():
            answers[question.id] = Answer.objects.filter(question=question.id).count()

    def new_questions(self):
        return self.objects.get_queryset().order_by('pub_date')

    def new_tag_questions(self, tag_slug):
        posts = Question.new_questions(self)
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
        return posts

    def hottest_questions(self):
        return self.objects.all()

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    votes = GenericRelation(Commend, related_query_name='articles')
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('дата публикации')

    def awsers_to_questions(self, question_id):
       return self.objects.get_queryset().filter(question=question_id).order_by('pub_date')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField(default='default.jpg', upload_to='user_images')

# Create your models here.
