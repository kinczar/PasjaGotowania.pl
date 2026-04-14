from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import DetailView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from .models import Comment
from main.models import Recipe

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

            post_type = request.POST.get("post_type")

            if post_type == "recipe":

                names = request.POST.getlist("ingredients_name[]")
                amounts = request.POST.getlist("ingredients_amount[]")
                units = request.POST.getlist("ingredients_unit[]")

                ingredients_list = []

                for name, amount, unit in zip(names, amounts, units):
                    if name:
                        ingredients_list.append(f"{name} - {amount} {unit}")

                if not ingredients_list:
                    return render(request, "forum/add_post.html", {
                        "form": form,
                        "error": "Dodaj przynajmniej jeden składnik"
                })

                post.ingredients = "\n".join(ingredients_list)

                post.calories = request.POST.get("calories") or None
                post.servings = request.POST.get("servings") or None

                time_value = request.POST.get("time_value")
                time_unit = request.POST.get("time_unit")

                if time_value:
                    post.time = f"{time_value} min"

            post.save()

            if post.post_type == "recipe":
                Recipe.objects.update_or_create(
                    forum_post_id=post.id,
                    defaults={
                        "title": post.title,
                        "description": post.body,
                        "ingredients": post.ingredients if post.ingredients else "",
                        "instructions": post.body,
                        "category": "Przepis z forum"
                    }
                )

            return redirect('/forum/')

    else:
        form = PostForm()

    return render(request, "forum/add_post.html", {
        "form": form
    })
    

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

    if request.method == 'POST': #odpowiadanie na posty
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user

        parent_id = request.POST.get("parent_id")
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


@login_required
def toggle_save(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.saved_by.all():
        post.saved_by.remove(request.user)
    else:
        post.saved_by.add(request.user)

    return redirect('forum')
