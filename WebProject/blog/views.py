import json
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views import View
from django.urls import reverse
from django.utils import timezone
from taggit.models import Tag
from .forms import add_post, add_answer, user_registration, user_setting
from .models import Question, Answer, Profile, Commend, ContentType


class VotesView(View):
    model = None  # Модель данных - Статьи или Комментарии
    vote_type = None  # Тип комментария Like/Dislike

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        # GenericForeignKey не поддерживает метод get_or_create
        try:
            likedislike = Commend.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id,
                                                  user=request.user)
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except Commend.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            result = True

        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.votes.likes().count(),
                "dislike_count": obj.votes.dislikes().count(),
                "sum_rating": obj.votes.sum_rating()
            }),
            content_type="application/json"
        )

def paginate(objects_list, request, obj_per_list = 5):
    paginator = Paginator(objects_list, obj_per_list)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    return items


def main(request, tag_slug=None):
    posts = Question.objects.get_queryset().order_by('-pub_date')
    title = 'Recent updates'
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
        title = '#' + str(tag)
    questions = paginate(posts, request, 4)
    answers = {}
    for question in Question.objects.all():
        answers[question.id] = Answer.objects.filter(question=question.id).count()

    profiles = Profile.objects.all()

    return render(request, 'blog/index.html', {'questions': questions,
                                               'title': title, 'answers': answers, 'profiles': profiles})


class AccauntSetting(View):
        def get(self, request):
            curr_acc = Profile.objects.get(username=request.user)
            form = user_setting(instance=curr_acc)
            return render(request, 'blog/user_settings.html', {'form': form})

        def post(self, request):
            form = user_setting(request.POST, request.FILES)
            if form.is_valid():
                user = Profile.objects.get(username=request.user)
                user.email = form.data.get("email")
                user.first_name = form.data.get("first_name")
                user.img = form.files.get("img", default= user.img)
                user.save()
                return HttpResponseRedirect(reverse('main_page'))
            return HttpResponseRedirect(reverse('settings'))
#
# def settings_done(request):
#   user = Profile.objects.get(username = request.user)
#   user.username = request.POST.get("login")
#   user.email = request.POST.get("email")
#   user.first_name = request.POST.get("nickname")
#   user.save()
#   return HttpResponseRedirect(reverse('main_page'))
#
# def settings(request):
#   return render(request,'blog/user_settings.html')

def some_post(request, question_id):
    try:
        post = Question.objects.get(id=question_id)
    except:
        raise Http404("Статья не найдена!")
    form = add_answer()
    commets = Answer.objects.get_queryset().filter(question = question_id).order_by('pub_date')
    commets = paginate(commets, request, 3)
    profiles = Profile.objects.all()
    return render(request, 'blog/single_post.html', {'post': post, 'comments': commets,
                                                      'profiles': profiles, 'form': form})

def leave_answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = add_answer(request.POST)
        if form.is_valid():
          answer = form.save(commit=False)
          answer.author_id = request.user
          answer.pub_date = timezone.now()
          answer.question = question
          answer.save()
          form.save_m2m()
          return HttpResponseRedirect(reverse('question_page', args = (question.id,)))
    else:
      form = add_answer()

    return render(request, 'blog/index.html')


def create_post(request):
    form = add_post()
    return render(request, 'blog/post_create.html', {'form': form})

def ask_question(request):
    if request.method == "POST":
        form = add_post(request.POST)
        if form.is_valid():
          question = form.save(commit=False)
          question.author_id = request.user
          question.pub_date = timezone.now()
          question.save()
          form.save_m2m()
          return HttpResponseRedirect(reverse('question_page', args = (question.id,)))

    else:
      form = add_post()

    return render(request, 'blog/index.html')

#def leave_answer(request, question_id):
 #   form = add_answer()
  #  return render(request, 'blog/post_create.html', {'form': form})
  #try:
   # question = Question.objects.get(id = question_id)
 # except:
  #  raise Http404("Статья не найдена!")
  #question.answer_set.create(author_id= request.user, text = request.POST['text'], pub_date = timezone.now())
  #return HttpResponseRedirect(reverse('question_page', args = (question.id,)))


class  Registration(View):
        def get(self, request):
            form = user_registration()
            return render(request, 'blog/singup.html', {'form': form})

        def post(self, request):
            form = user_registration(request.POST, request.FILES)
            if form.is_valid():
                acc = form.save(commit=False)
                acc.is_active = True
                acc.set_password(acc.password)
                acc.save()
                form.save()
                return HttpResponseRedirect(reverse('login'))
            return HttpResponseRedirect(reverse('singup'))


def test(request):
    return render(request, 'blog/test.html', {})

def singup(request):
    return render(request, 'blog/singup.html', {})

def singin(request):
    return render(request, 'blog/singin.html', {})

def user_settrings(request):
    return render(request, 'blog/user_settings.html', {})
# Create your views here.
