from django.contrib import admin
from django.urls import path,include
from blogapp import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',views.signup,name='signup'),
    path('display/',views.Display,name='display'),
    path('add/',views.Add,name='add'),
    path('myposts/',views.MyPosts,name='myposts'),
    path('delete/<int:id>',views.Delete,name='delete'),
    path('edit/<int:id>',views.Edit,name='edit'),
    path('like/<int:id>',views.like_post,name='like_post'),
    path('comment/',views.Comment,name='comment'),
    path('post-detail/<int:id>',views.PostDetail,name='post_detail'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('',views.home,name= 'home'),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/change-password.html',
            success_url = '/'
        ),
        name='change_password'
    ),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)



