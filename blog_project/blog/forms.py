from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Post, Comment


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages["invalid_login"] = (
            "ユーザー名またはパスワードが正しくありません。"
        )


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "コメントを入力",
                }
            ),
        }


from .models import Profile


class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_image"]
        labels = {"profile_image": "プロフィール画像"}
