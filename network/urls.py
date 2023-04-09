
from django.urls import path

from . import views
from rest_framework.authtoken.views import obtain_auth_token
#need to be able to upload images
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost", views.newPost, name="newPost"),
    path("<str:userName>", views.profilePage, name="profilePage"),
    path("<str:userName>/connection", views.connection, name="connection"),
    path("networks/following", views.following, name="following"),
    path("networks/<int:postID>/editPost", views.editPost, name="editPost"),
    path("networks/<int:postID>/likePost", views.likePost, name="likePost"),
    path("<str:userName>/editProfile", views.editProfile, name="editProfile"),
    
]

#if settings.DEBUG:
        #urlpatterns += static(settings.MEDIA_URL,
                              #document_root=settings.MEDIA_ROOT)
#urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
