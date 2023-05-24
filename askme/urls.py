from django.contrib import admin
from django.urls import path

from django.conf.urls.static import static
from django.conf import settings
import sys
sys.path.append('../app/')

from app import views

urlpatterns = [
    path('', views.index, name="root"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('signup/', views.signup, name="signup"),
    path('ask/', views.ask, name="ask"),
    path('question/<int:question_id>', views.question, name="question"),
    path('tag/<str:tag_name>', views.tag, name="tag"),
    path('hot/', views.hot, name="hot"),
    path('admin/', admin.site.urls, name="admin"),
    path('profile/edit/', views.profile_edit, name="profile_edit"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
