from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import DetailView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import CommentForm

# Create your views here.
def index(request):
    return render(request,'forum/index.html') 

def frequent_questions(request):
    return render(request,'forum/frequent_questions.html')
     

def forum(request):
    posts = Post.objects.all().order_by('-published_at') #posty wyswietlaja sie od najnowszego
    return render(request, 'forum/forum.html', {'posts': posts})

#dodawanie posta
@login_required
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect('/forum/')
    else:
        form = PostForm()

    return render(request, "forum/add_post.html", {"form": form})

#usuwanie posta
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author == request.user:
        post.delete()

    return redirect('forum')

#kod na dodawanie like do postow
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('forum')

#dodawanie komentarzy tylko dla zalogowanych
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

    return redirect('forum')
