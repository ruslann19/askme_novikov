from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from django.core.paginator import Paginator
from django.http import *

from app.models import *

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from app.forms import *

# ----------------------------------------

PER_PAGE = 10

def paginate(objects_list, page=1, per_page=PER_PAGE):
    paginator = Paginator(objects_list, per_page)

    try:
        page_number = int(page)
    except ValueError:
        page_number = 1

    if page_number < 1 or page_number > paginator.num_pages:
        page_number = 1
    
    page = paginator.page(page_number)
    return page

# ----------------------------------------

def index(request):
    page = paginate(Question.objects.new(), request.GET.get("page", 1))

    context = {
        "questions": page.object_list,
        "page_obj": page,
        "popular_tags": Tag.objects.popular(),
    }
    if not request.user.is_anonymous:
        context["profile"] = request.user.profile
    return render(request, "index.html", context)


def hot(request):
    page = paginate(Question.objects.hot(), request.GET.get("page", 1))
    context = {
        "questions": page.object_list,
        "page_obj": page,
        "popular_tags": Tag.objects.popular(),
    }
    if not request.user.is_anonymous:
        context["profile"] = request.user.profile
    return render(request, "hot.html", context)


def tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)

    questions_with_tag = Question.objects.get_questions_with_tag(tag)
    
    page = paginate(questions_with_tag, request.GET.get("page", 1))
    context = {
        "tag_name": tag.name,
        "questions": page.object_list,
        "page_obj": page,
        "popular_tags": Tag.objects.popular(),
    }
    if not request.user.is_anonymous:
        context["profile"] = request.user.profile
    return render(request, "tag.html", context)


@login_required
def my_questions(request):
    page = paginate(Question.objects.filter(author=request.user.profile), request.GET.get("page", 1))

    context = {
        "questions": page.object_list,
        "page_obj": page,
        "popular_tags": Tag.objects.popular(),
    }
    if not request.user.is_anonymous:
        context["profile"] = request.user.profile
    return render(request, "my_questions.html", context)


def question(request, id, page_number=1):
    if request.method == "GET":
        question = Question.objects.get(pk=id)
        page = paginate(question.answers.all().order_by("created_at"), request.GET.get("page", 1))

        form = AnswerForm(initial={"question_id": id})

    elif request.method == "POST":
        form = AnswerForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            profile = Profile.objects.get(user=request.user)
            question = Question.objects.get(id=data.get("question_id"))

            answer = Answer(
                question=question,
                text=data.get("text"),
                author=profile,
            )
            answer.save()

            page = paginate(question.answers.all().order_by("-created_at"), page=1)
            page_number = page.paginator.num_pages

            return redirect(
                reverse(
                    "question", 
                    kwargs={
                        "id": question.id,
                    }
                ) + f"?page={page_number}#answer_{answer.id}"
            )

    context = {
        "question": question,
        "answers": page.object_list,
        "page_obj": page,
        "popular_tags": Tag.objects.popular(),
        "form": form,
    }
    if not request.user.is_anonymous:
        context["profile"] = request.user.profile
    return render(request, "question.html", context)


def login(request):
    if request.method == "GET":
        next_page = request.GET.get("next", "index")
        form = LoginForm(initial={"next_page": next_page})
    
    elif request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(request.POST.get("next_page"))

            form.add_error("username", "Invalid username or password")
            form.add_error("password", "Invalid username or password")
    
    context = {
        "popular_tags": Tag.objects.popular(),
        "form": form,
    }
    return render(request, "login.html", context)


@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('index'))


def signup(request):
    if request.method == "GET":
        user_form = UserForm()
        profile_form = ProfileForm()
    
    elif request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            auth.login(request, user)

            return redirect(reverse("index"))

    context = {
        "popular_tags": Tag.objects.popular(),
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "signup.html", context)


@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "GET":
        user_form = EditUserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    elif request.method == "POST":
        user_form = EditUserForm(data=request.POST, instance=request.user)
        profile_form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = Profile.objects.get(user=user)
            
            if profile_form.cleaned_data.get("avatar") == False:
                profile.avatar.delete()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

        return HttpResponseRedirect(request.path_info)

    context = {
        "profile": request.user.profile,
        "popular_tags": Tag.objects.popular(),
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "edit_profile.html", context)


@login_required
def change_password(request):
    if request.method == "GET":
        form = PasswordForm()

    elif request.method == "POST":
        form = PasswordForm(data=request.POST)

        if form.is_valid():
            password = form.cleaned_data.get("password")
            user = request.user
            user.set_password(password)
            user.save()
            auth.login(request, user)
        
            return redirect(reverse("edit_profile"))
    
    context = {
        "profile": request.user.profile,
        "popular_tags": Tag.objects.popular(),
        "form": form,
    }
    return render(request, "change_password.html", context)


@login_required
def ask(request):
    if request.method == "GET":
        form = QuestionForm()

    elif request.method == "POST":
        form = QuestionForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            profile = Profile.objects.get(user=request.user)
            
            question = Question( 
                title=data.get("title"),
                text=data.get("text"),
                author=profile,
            )
            question.save()

            for tag in data.get("tags"):
                question.tags.add(tag)
            question.save()

            return redirect(f"/question/{question.id}/")

    context = {
        "profile": request.user.profile,
        "popular_tags": Tag.objects.popular(),
        "form": form,
    }
    return render(request, "ask.html", context)


@require_POST
@login_required
def like_question(request, question_id):
    question = Question.objects.get(id=question_id)
    profile = request.user.profile
    value = (request.POST.get("action") == "Like")

    exists = QuestionLike.objects.filter(question=question, profile=profile).exists()

    if exists:
        question_like = QuestionLike.objects.get(question=question, profile=profile)
        stored_value = question_like.value

        if stored_value == value:
            question_like.delete()
        else:
            question_like.delete()
            QuestionLike.objects.create(
                question=question,
                profile=profile,
                value=value
            )
    else:
        QuestionLike.objects.create(
            question=question,
            profile=profile,
            value=value
        )

    next = request.POST.get("next", "/")
    return HttpResponseRedirect(next)


@require_POST
@login_required
def like_answer(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    profile = request.user.profile
    value = (request.POST.get("action") == "Like")

    exists = AnswerLike.objects.filter(answer=answer, profile=profile).exists()

    if exists:
        answer_like = AnswerLike.objects.get(answer=answer, profile=profile)
        stored_value = answer_like.value

        if stored_value == value:
            answer_like.delete()
        else:
            answer_like.delete()
            AnswerLike.objects.create(
                answer=answer,
                profile=profile,
                value=value
            )
    else:
        AnswerLike.objects.create(
            answer=answer,
            profile=profile,
            value=value
        )

    next = request.POST.get("next", "/")
    return HttpResponseRedirect(next)


@require_POST
@login_required
def correct_answer(request, answer_id):
    answer = Answer.objects.get(id=answer_id)

    answers = answer.question.answers
    
    exists = answers.filter(is_correct=True).exists()

    if exists:
        previous_correct = answers.get(is_correct=True)
        if previous_correct == answer:
            previous_correct.is_correct = False
            answer.is_correct = False
        else:
            previous_correct.is_correct = False
            answer.is_correct = True
    
        previous_correct.save()
    else:
        answer.is_correct = True
    
    answer.save()

    next = request.POST.get("next", "/")
    return HttpResponseRedirect(next)