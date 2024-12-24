from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db.models import Count

class TagManager(models.Manager):
    def popular(self):
        return self.annotate(cnt=Count('questions')).order_by('-cnt')[:5]


class Tag(models.Model):
    name = models.CharField(max_length=32)

    objects = TagManager()

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="./uploads/", blank=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class QuestionManager(models.Manager):
    def new(self):
        return self.all().order_by("-created_at")
    
    def hot(self):
        # return self.all().order_by("-rating")
        return self.all().order_by("created_at")
    
    def get_questions_with_tag(self, tag):
        return self.filter(tags=tag).order_by("-rating")


class Question(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField(max_length=2048)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="questions")
    rating = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name="questions", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = QuestionManager()

    def __str__(self):
        return self.title
    
    def likes_count(self):
        return self.likes.all().filter(value=True).count()
    
    def dislikes_count(self):
        return self.likes.all().filter(value=False).count()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.TextField(max_length=2048)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="answers")
    rating = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Answer from {self.author} on question \"{self.question}\""
    
    def likes_count(self):
        return self.likes.all().filter(value=True).count()
    
    def dislikes_count(self):
        return self.likes.all().filter(value=False).count()


class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="question_likes")
    value = models.BooleanField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["question", "user"], name="unique_question_like")
        ]

    def __str__(self):
        return f"{self.question}, {self.user}"


class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="answer_likes")
    value = models.BooleanField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["answer", "user"], name="unique_answer_like")
        ]

    def __str__(self):
        return f"{self.answer}, {self.user}"
