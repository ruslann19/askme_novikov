from django.shortcuts import render

from django.core.paginator import Paginator
from django.http import *

# Create your views here.

user = {
    "is_authenticated": True
}

TAGS_BEGIN = 1
TAGS_END = 1 + 5
tags = []
for i in range(TAGS_BEGIN, TAGS_END):
    tags.append(f"tag_{i}")

QUESTIONS_BEGIN = 1
QUESTIONS_END = 1 + 30
questions = []
for i in range(QUESTIONS_BEGIN, QUESTIONS_END):
    questions.append({
        "title": f"Title {i}",
        "id": i,
        "text": f"Text {i}",
        "likes": i,
        "dislikes": 0,
        "answers": i,
        "tags": tags,
    })

hot_questions = list(reversed(questions))

ANSWERS_BEGIN = 1
ANSWERS_END = 1 + 30
answers = []
for i in range(ANSWERS_BEGIN, ANSWERS_END):
    answers.append({
        "text": f"Answer {i}",
    })

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
    page = paginate(questions, request)
    context = {
        "user": user,
        "questions": page.object_list,
        "page_obj": page,
        "tags": tags,
    }
    return render(request, "index.html", context)

def hot(request):
    page = paginate(hot_questions, request)
    context = {
        "user": user,
        "questions": page.object_list,
        "page_obj": page,
        "tags": tags,
    }
    return render(request, "hot.html", context)

def tag(request, tag_name):
    tag_questions = []
    for question in questions:
        if tag_name in question["tags"]:
            tag_questions.append(question)

    page = paginate(tag_questions, request)
    context = {
        "user": user,
        "tag_name": tag_name,
        "questions": page.object_list,
        "page_obj": page,
        "tags": tags,
    }
    return render(request, "tag.html", context)

def question(request, id):
    try:
        id = int(id)
        if id < 1 or id > len(questions):
            return HttpResponseNotFound()
    except ValueError:
        return HttpResponseNotFound()
    
    question = questions[id - 1]
    page = paginate(answers, request)
    context = {
        "user": user,
        "question": question,
        "answers": page.object_list,
        "page_obj": page,
        "tags": tags,
    }
    return render(request, "question.html", context)

def login(request):
    context = {
        "user": user
    }
    return render(request, "login.html", context)

def signup(request):
    context = {
        "user": user
    }
    return render(request, "signup.html", context)

def ask(request):
    context = {
        "user": user
    }
    return render(request, "ask.html", context)
