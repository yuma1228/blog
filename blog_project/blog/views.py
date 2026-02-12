from django.http import HttpResponse
from .models import Post, Comment, Profile
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import SignUpForm, LoginForm, CreatePostForm, CommentForm, ProfileImageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as BaseLoginView
from django.urls import reverse_lazy, reverse
from django.core.exceptions import ValidationError

# ログイン前のトップページ
# ここでは、いまのところ全ての投稿を表示する


class IndexView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.order_by("-created_at")[:3]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_posts"] = Post.objects.all().order_by("-created_at")
        return context


# ログイン後のトップページ
class HomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.order_by("-created_at")[:3]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["user"] = self.request.user
        context["all_posts"] = Post.objects.all().order_by("-created_at")
        return context


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("Blog:index")
    else:
        form = SignUpForm()

    return render(request, "blog/signup.html", {"form": form})


class LoginView(BaseLoginView):
    form_class = LoginForm
    template_name = "blog/login.html"


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        """ページ表示（GETリクエスト）の際に、テンプレートに渡すデータを追加するメソッド"""
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class MyPageView(LoginRequiredMixin, ListView):
    paginate_by = 6
    model = Post
    template_name = "blog/mypage.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        # プロフィールが存在しない場合は作成
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        context["profile"] = profile
        context["profile_form"] = ProfileImageForm(instance=profile)

        # ユーザーのコメント一覧を追加
        context["user_comments"] = (
            Comment.objects.filter(author=self.request.user)
            .select_related("post")
            .order_by("-created_at")[:10]
        )

        # 統計情報を追加
        context["post_count"] = Post.objects.filter(author=self.request.user).count()
        context["comment_count"] = Comment.objects.filter(
            author=self.request.user
        ).count()

        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = "blog/post_create.html"
    success_url = reverse_lazy("Blog:mypage")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "ポストが作成されました！")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "内容を正しく入力してください。")
        return super().form_invalid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("Blog:mypage")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse_lazy("Blog:post_detail", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/post_detail.html"

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            messages.error(self.request, "コメントするにはログインしてください。")
            return redirect("Blog:login")
        else:
            post = get_object_or_404(Post, pk=self.kwargs["pk"])
            form.instance.post = post
            form.instance.author = self.request.user
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("Blog:post_detail", kwargs={"pk": self.kwargs["pk"]})


@login_required
def update_profile_image(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileImageForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "プロフィール画像を更新しました！")
        else:
            messages.error(request, "画像のアップロードに失敗しました。")

    return redirect("Blog:mypage")
