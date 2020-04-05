from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils import timezone
from taggit.models import Tag
from .forms import add_post
from .models import Question, Answer

def paginate(objects_list, request, obj_per_list = 5):
    paginator = Paginator(objects_list, obj_per_list)
    page = request.GET.get('page')
    items = paginator.get_page(page)
    return items


def main(request, tag_slug=None):
    posts = Question.objects.get_queryset().order_by('pub_date')
    title = 'Recent updates'
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
        title = '#' + str(tag)
    questions = paginate(posts, request, 3)
    answers = {}
    for question in Question.objects.all():
        answers[question.id] = Answer.objects.filter(question=question.id).count()
    return render(request, 'blog/index.html', {'questions': questions, 'title': title, 'answers': answers})

def settings_done(request):
  user = User.objects.get(username = request.user)
  user.username = request.POST.get("login")
  user.email = request.POST.get("email")
  user.first_name = request.POST.get("nickname")
  user.save()
  return HttpResponseRedirect(reverse('main_page'))

def settings(request):
  return render(request,'blog/user_settings.html')

def some_post(request, question_id):
    try:
        post = Question.objects.get(id=question_id)
    except:
        raise Http404("Статья не найдена!")
    commets = Answer.objects.get_queryset().filter(question = question_id).order_by('pub_date')
    commets = paginate(commets, request, 3)
    return render(request, 'blog/single_post.html', {'post': post, 'comments': commets})


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

def leave_answer(request, question_id):
  try:
    question = Question.objects.get(id = question_id)
  except:
    raise Http404("Статья не найдена!")
  question.answer_set.create(author_id= request.user, text = request.POST['text'], pub_date = timezone.now())
  return HttpResponseRedirect(reverse('question_page', args = (question.id,)))


def create_accaunt_add(request):
  user = User.objects.create_user(username=request.POST['login'], email=request.POST['email'],
                                  password=request.POST['password'], first_name=request.POST['nickname'])
  user.save()
  return HttpResponseRedirect(reverse('login'))


def create_accaunt(request):
  return render(request, 'blog/singup.html')
# Create your views here.



def test(request):
    return render(request, 'blog/test.html', {})

def singup(request):
    return render(request, 'blog/singup.html', {})

def singin(request):
    return render(request, 'blog/singin.html', {})

def user_settrings(request):
    return render(request, 'blog/user_settings.html', {})
# Create your views here.
