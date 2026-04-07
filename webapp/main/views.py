# Plik do definiowania widoków, które są renderowane za pomocą szablonizatora Jinja oraz wyświetlane w przeglądarce

from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages #to show message back for errors
from django.contrib.auth.decorators import login_required

from .models import Recipe

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

@login_required
def cars(request):
    values = {
        'cars': [
            {
                'car': 'Nissan 350Z',
                'year': 2003,
                'drive_wheel': 'rwd',
                'color': 'orange',
                'price': '$35,000',
            },
            {
                'car': 'Mitsubishi Lancer Evolution VIII',
                'year': 2004,
                'drive_wheel': '4wd',
                'color': 'yellow',
                'price': '$36,000',
            },
            {
                'car': 'Ford Mustang GT (Gen. 5)',
                'year': 2005,
                'drive_wheel': 'rwd',
                'color': 'red',
                'price': '$36,000',
            },
            {
                'car': 'BMW M3 GTR (E46)',
                'year': 2005,
                'drive_wheel': 'rwd',
                'color': 'blue and gray',
                'price': 'Priceless',
            },
        ]
    }

    return render(request, 'main/cars.html', values)

def about(request):
    return render(request, 'main/about.html')

# Using the Django authentication system (Django Documentation)
# https://docs.djangoproject.com/en/5.1/topics/auth/default/
def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
     
    if request.method == 'POST':
         user = authenticate(username=request.POST['username'], password=request.POST['password'])
         if user is not None:
             login(request, user)
             if request.session.get('next'):
                return redirect(request.session.pop('next'))
             
             return redirect('home')
         else:
             messages.error(request, 'Invalid credentials')
             return redirect('login_user')
         
    if request.GET.get('next'):
        request.session['next'] = request.GET['next']

    return render(request, 'main/users/login.html')

def register(request):
    if request.user.is_authenticated:
         return redirect('home')
    
    if request.method == 'POST':
        user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
        login(request, user)
        return redirect('home')
    
    return render(request, 'main/users/register.html')

def logout_user(request):
    logout(request)
     
    return redirect('home')

def recipes(request):
    query = request.GET.get("q")
    category = request.GET.get("category")
    results = []
    favorite_ids = []

    if query or category:
        results = Recipe.objects.all()

        if query:
            results = results.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__icontains=query) |
                Q(ingredients__icontains=query)
            )

        if category:
            results = results.filter(category__icontains=category)

    if request.user.is_authenticated:
        favorite_ids = request.user.favorite_recipes.values_list('id', flat=True)

    return render(request, "main/recipes.html", {
        "query": query,
        "results": results,
        "category": category,
        "favorite_ids": favorite_ids,
    })

def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'main/detail.html', {'recipe': recipe})

@login_required
def toggle_favorite(request, id):
    recipe = get_object_or_404(Recipe, id=id)

    if request.user in recipe.favorites.all():
        recipe.favorites.remove(request.user)
    else:
        recipe.favorites.add(request.user)

    return redirect('recipes')

def health(request):
    return render(request, 'main/health.html')

@login_required
def recipes(request):
    saved_posts = request.user.saved_posts.all()

    return render(request, "main/recipes.html", {
        "saved_posts": saved_posts
    })
