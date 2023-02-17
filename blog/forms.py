from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {
            "published_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
        fields = ("title", "text", "published_date", "tags")
