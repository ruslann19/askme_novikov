"""
URL configuration for askme_novikov project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.urls import include

from app import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),

    path("",                             views.index,        name="index"),
    path("hot/",                         views.hot,          name="hot"),
    path("tag/<str:tag_name>/",          views.tag,          name="tag"),
    path("question/<int:id>/",           views.question,     name="question"),
    
    path("login/",                       views.login,        name="login"),
    path("logout/",                      views.logout,       name="logout"),
    path("signup/",                      views.signup,       name="signup"),
    path("profile/edit/",                views.edit_profile, name="edit_profile"),
    path("profile/edit/password/",       views.change_password, name="change_password"),
    
    path("ask/",                         views.ask,          name="ask"),

    path("like_question/<int:question_id>", views.like_question, name="like_question"),
    path("like_answer/<int:answer_id>", views.like_question, name="like_answer"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
