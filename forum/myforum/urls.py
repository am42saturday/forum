from django.urls import path, include
from django.conf import settings

from . import views

app_name = 'myforum'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', view=views.LoginView.as_view(), name='login'),
    path('logout/', view=views.LogoutView.as_view(), name='logout'),
    path('<int:topic_id>/', views.TopicView.as_view(), name='topic'),
    path('profile/<int:user_id>/', views.ProfileView.as_view(), name='profile'),
    path('new/', views.TopicCreate.as_view(), name='create'),
    path('register/', views.RegisterView.as_view(), name='register'),
]

# if settings.DEBUG:
#     import debug_toolbar
#
#     urlpatterns += [
#         path(r'__debug__/', include(debug_toolbar.urls)),
#     ]
