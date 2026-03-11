from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import DetailView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm

# Create your views here.
def index(request):
    return render(request,'forum/index.html') 

def frequent_questions(request):
    return render(request,'forum/frequent_questions.html')
     

def forum(request):
    posts = Post.objects.all()
    return render(request, 'forum/forum.html', {'posts': posts})

def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/forum')
    else:
        form = PostForm()

    return render(request, 'forum/add_post.html', {'form': form})