from django.utils import timezone
from django.views import generic
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User, Topic, Comment

# Показывать ошибку, если пользователь не найден или парол не соответствует
class RegisterView(TemplateView):
    template_name = 'myforum/register.html'

    def post(self, request, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('myforum:index'))
        first_name = request.POST.get("first-name")
        last_name = request.POST.get("last-name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(password)
        email = request.POST.get("email")
        # avatar = request.POST.get("avatar")
        user = User(first_name=first_name, last_name=last_name, username=username,
            password=password, email=email, date_joined=timezone.now(),
            last_login = timezone.now())
        user.save()
        user = authenticate(username=username, password=password)
        login(request, user)
        return HttpResponseRedirect(reverse('myforum:index'))


class LoginView(TemplateView):
    template_name = 'myforum/login.html'

    def post(self, request, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('myforum:index'))
        if request.method == 'POST':
            user = authenticate(username=request.POST.get("login"), password=request.POST.get("password"))
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('myforum:index'))
            else:
                print("User not found")
                return render(request, 'myforum/login.html')
        else:
            return render(request, 'myforum/login.html')


class LogoutView(TemplateView):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('myforum:login'))


class IndexView(generic.ListView):
    template_name = 'myforum/index.html'
    context_object_name = "latest_topic_list"

    def get_queryset(self):
        return Topic.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class TopicView(TemplateView):
    template_name = 'myforum/topic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic'] = Topic.objects.get(id=context['topic_id'])
        return context

    def post(self, request, **kwargs):
        if request.user.is_authenticated:
            user = request.user.id
            topic_id = kwargs["topic_id"]
            pub_date = timezone.now()
            text = request.POST.get("leave-comment")
            new_comment = Comment(author=User.objects.get(id=user), pub_date=pub_date,
                topic=Topic.objects.get(id=topic_id), text=text)
            new_comment.save()
            topic = Topic.objects.get(id=topic_id)
            topic.last_activity_date = pub_date
            topic.save()
            return self.get(request, **kwargs)
        else:
            return render(request, 'myforum/login.html')


class ProfileView(TemplateView):
    template_name = 'myforum/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context['user_id']
        print(context)
        print(user)
        context['user'] = User.objects.get(id=user)
        return context


class TopicCreate(TemplateView):
    template_name = 'myforum/create_topic.html'

    def post(self, request):
        if request.user.is_authenticated:
            user = request.user.id
            title = request.POST.get("topic-title")
            text = request.POST.get("topic-text")
            new_topic = Topic(author=User.objects.get(id=user), pub_date=timezone.now(),
                last_activity_date=timezone.now(), title=title, text=text)
            new_topic.save()
            print(reverse('myforum:topic', args=[new_topic.id]))
            return HttpResponseRedirect(reverse('myforum:topic', args=[new_topic.id]))
        else:
            return render(request, 'myforum/login.html')
