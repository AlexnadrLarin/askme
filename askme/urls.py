from django.contrib import admin
from django.urls import path
import sys
sys.path.append('../app/')
from app import views

urlpatterns = [
    path('', views.index, name="root"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('ask/', views.ask, name="ask"),
    path('settings/', views.settings, name="settings"),
    path('question/<int:question_id>', views.question, name="question"),
    path('tag/<str:tag_name>', views.tag, name="tag"),
    path('hot/', views.hot, name="hot"),
    path('admin/', admin.site.urls, name="admin"),
]
