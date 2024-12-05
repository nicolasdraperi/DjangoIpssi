from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost, Comment
from .forms import BlogPostForm, CommentForm


def post_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comments = Comment.objects.filter(post=post)
    return render(request, 'post_detail.html', {'post': post, 'comments': comments})


def add_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            BlogPost.objects.create(title=title, content=content)
            return HttpResponseRedirect("/")
    else:
        form = BlogPostForm()

    return render(request, "add_post.html", {"form": form})


def edit_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post.title = form.cleaned_data["title"]
            post.content = form.cleaned_data["content"]
            post.save()
            return HttpResponseRedirect(f"/post/{pk}/")
    else:
        form = BlogPostForm(initial={"title": post.title, "content": post.content})

    return render(request, "edit_post.html", {"form": form})


def add_comment(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            author = form.cleaned_data["author"]
            text = form.cleaned_data["text"]
            Comment.objects.create(post=post, author=author, text=text)
            return HttpResponseRedirect(f"/post/{pk}/")
    else:
        form = CommentForm()

    return render(request, "add_comment.html", {"form": form})


def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment.text = form.cleaned_data["text"]
            comment.author = form.cleaned_data["author"]
            comment.save()
            return HttpResponseRedirect(f"/post/{comment.post.id}/")
    else:
        form = CommentForm(initial={"author": comment.author, "text": comment.text})

    return render(request, "edit_comment.html", {"form": form, "comment": comment})



def delete_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'delete_post.html', {'post': post})


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        post_pk = comment.post.pk
        comment.delete()
        return redirect('post_detail', pk=post_pk)
    return render(request, 'delete_comment.html', {'comment': comment})
