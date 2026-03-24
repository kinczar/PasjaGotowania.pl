from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import DetailView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from .models import Comment

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

    parent_id = request.POST.get("parent_id") #odpowiadanie na komentarze
    if parent_id:
        parent = Comment.objects.get(id=parent_id)
        comment.parent = parent

    comment.save()

    return redirect('forum')

def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user.is_authenticated:
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
    
    return redirect('forum')

from django.contrib.auth.decorators import login_required

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author == request.user:
        comment.delete()

    return redirect('forum')
