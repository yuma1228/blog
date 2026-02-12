from django.urls import path, include
from django.contrib.auth.views import LogoutView, LoginView
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "Blog"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("home/", views.HomeView.as_view(), name="home"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path(
        "login/",
        views.LoginView.as_view(
            redirect_authenticated_user=True, template_name="blog/login.html"
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", views.signup_view, name="signup"),
    path("mypage/", views.MyPageView.as_view(), name="mypage"),
    path("create/", views.CreatePostView.as_view(), name="post_create"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
    path(
        "comment/<int:pk>/delete/",
        views.CommentDeleteView.as_view(),
        name="comment_delete",
    ),
    path(
        "post/<int:pk>/comment/",
        views.CommentCreateView.as_view(),
        name="comment_create",
    ),
    path("profile/update/", views.update_profile_image, name="update_profile_image"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
