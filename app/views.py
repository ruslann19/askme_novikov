from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator
from django.http import *

from app.models import *

# Create your views here.

user = {
    "is_authenticated": True
}

# ----------------------------------------

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)

    try:
        page_number = int(request.GET.get("page", 1))
    except ValueError:
        page_number = 1

    if page_number < 1 or page_number > paginator.num_pages:
        page_number = 1
    
    page = paginator.page(page_number)
    return page

# ----------------------------------------

def index(request):
    page = paginate(Question.objects.new(), request)
    context = {
        "user": user,
        "questions": page.object_list,
        "page_obj": page,
        "popular_tags": Tag.objects.popular(),
    }
    return render(request, "index.html", context)

def hot(request):
    page = paginate(Question.objects.hot(), request)
    context = {
        "user": user,
        "questions": page.object_list,
        "page_obj": page,
        "popular_tags": Tag.objects.popular(),
    }
    return render(request, "hot.html", context)

def tag(request: HttpRequest, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)

    questions_with_tag = Question.objects.get_questions_with_tag(tag)
    
    page = paginate(questions_with_tag, request)
    context = {
        "user": user,
        "tag_name": tag.name,
        "questions": page.object_list,
        "page_obj": page,
        "popular_tags": Tag.objects.popular(),
    }
    return render(request, "tag.html", context)


def question(request, id):
    question = Question.objects.get(pk=id)
    print(question)
    page = paginate(question.answers.all(), request)
    context = {
        "user": user,
        "question": question,
        "answers": page.object_list,
        "page_obj": page,
        "popular_tags": Tag.objects.popular(),
    }
    return render(request, "question.html", context)

def login(request):
    context = {
        "user": user,
        "popular_tags": Tag.objects.popular(),
    }
    return render(request, "login.html", context)

def signup(request):
    context = {
        "user": user,
        "popular_tags": Tag.objects.popular(),
    }
    return render(request, "signup.html", context)

def ask(request):
    context = {
        "user": user,
        "popular_tags": Tag.objects.popular(),
    }
    return render(request, "ask.html", context)
