from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import generic
from .models import Post
from .forms import PostForm


# Create your views here.
def post_list(request):
    to_publish = Post.objects.exclude(published_date__lte=timezone.now())

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
        "published_date"
    )
    return render(
        request,
        "blog/post_list.html",
        {"posts": posts, "to_publish": to_publish, "title": "Página principal"},
    )


class PostListView(generic.ListView):
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(published_date__lte=timezone.now()).order_by(
        "published_date"
    )

    def get_context_data(self, **kwargs):
        if self.request.GET:
            tags = self.request.GET.get("tags", None)
            context = super().get_context_data(**kwargs)

            to_publish_tagged = Post.objects.exclude(
                published_date__lte=timezone.now()
            ).filter(tags__icontains=tags.strip())

            posts_tagged = Post.objects.filter(
                tags__icontains=tags.strip(), published_date__lte=timezone.now()
            ).order_by("published_date")

            context["to_publish"] = to_publish_tagged
            context["posts"] = posts_tagged

            return context

        context = super().get_context_data(**kwargs)
        context["to_publish"] = Post.objects.exclude(published_date__lte=timezone.now())

        return context


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, "blog/post_detail.html", {"post": post, "title": post.title})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            if form.cleaned_data["published_date"] <= timezone.now():
                return redirect("post_detail", slug=post.slug)
            else:
                return redirect("post_list")

    else:
        form = PostForm()

    form = PostForm()
    return render(request, "blog/post_edit.html", {"form": form})


def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect("post_detail", slug=post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, "blog/post_edit.html", {"form": form})
