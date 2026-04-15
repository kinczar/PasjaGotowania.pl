<<<<<<< Updated upstream
# Plik do definiowania widoków, które są renderowane za pomocą szablonizatora Jinja oraz wyświetlane w przeglądarce

from django.http import HttpResponse
=======
from django.http import HttpResponse, JsonResponse
>>>>>>> Stashed changes
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages #to show message back for errors
from django.contrib.auth.decorators import login_required
<<<<<<< Updated upstream

from .models import Recipe
=======
from difflib import get_close_matches
import unicodedata
import re
import json

from forum.models import Post
from .models import Recipe

>>>>>>> Stashed changes

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

@login_required
def cars(request):
    values = {
        'cars': [
            {'car': 'Nissan 350Z', 'year': 2003, 'drive_wheel': 'rwd', 'color': 'orange', 'price': '$35,000'},
            {'car': 'Mitsubishi Lancer Evolution VIII', 'year': 2004, 'drive_wheel': '4wd', 'color': 'yellow', 'price': '$36,000'},
            {'car': 'Ford Mustang GT (Gen. 5)', 'year': 2005, 'drive_wheel': 'rwd', 'color': 'red', 'price': '$36,000'},
            {'car': 'BMW M3 GTR (E46)', 'year': 2005, 'drive_wheel': 'rwd', 'color': 'blue and gray', 'price': 'Priceless'},
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
<<<<<<< Updated upstream
         user = authenticate(username=request.POST['username'], password=request.POST['password'])
         if user is not None:
             login(request, user)
             if request.session.get('next'):
=======
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user:
            login(request, user)

            if request.session.get('next'):
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
        user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
=======
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email:
            messages.error(request, "Email jest wymagany")
            return render(request, 'main/users/register.html', {'username': username, 'email': email})

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.error(request, "Podaj poprawny email")
            return render(request, 'main/users/register.html', {'username': username, 'email': email})

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email zajęty")
            return render(request, 'main/users/register.html', {'username': username, 'email': email})

        if User.objects.filter(username=username).exists():
            messages.error(request, "Login zajęty")
            return render(request, 'main/users/register.html', {'username': username, 'email': email})

        if len(password) < 8:
            messages.error(request, "Hasło za krótkie")
            return render(request, 'main/users/register.html', {'username': username, 'email': email})

        user = User.objects.create_user(username=username, email=email, password=password)
>>>>>>> Stashed changes
        login(request, user)
        return redirect('home')
    
    return render(request, 'main/users/register.html')

def logout_user(request):
    logout(request)
     
    return redirect('home')

<<<<<<< Updated upstream
def recipes(request):
    query = request.GET.get("q")
    category = request.GET.get("category")
    results = []

    if query or category:
        results = Recipe.objects.all()

        if query:
            results = results.filter(title__icontains=query)

        if category:
            results = results.filter(category__icontains=category)

    return render(request, "main/recipes.html", {
        "query": query,
        "results": results,
        "category": category,
=======

def normalize_text(text):
    text = text.lower().strip()
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    return text


def recipes(request):
    query = request.GET.get("q", "").strip()
    results = Recipe.objects.all()

    if query:
        results = results.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(ingredients__icontains=query)
        ).distinct()

    return render(request, "main/recipes.html", {
        "query": query,
        "results": results
>>>>>>> Stashed changes
    })
def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'main/detail.html', {'recipe': recipe})
<<<<<<< Updated upstream
def health(request):
    return render(request, 'main/health.html')
=======


@login_required
def toggle_favorite(request, id):
    recipe = get_object_or_404(Recipe, id=id)

    if request.user in recipe.favorites.all():
        recipe.favorites.remove(request.user)
    else:
        recipe.favorites.add(request.user)

    return redirect('recipes')


def health(request):
    return render(request, "main/health.html")


# 🔥 AJAX BMI
def calculate_bmi(request):
    data = json.loads(request.body)

    height = float(data.get("height"))
    weight = float(data.get("weight"))

    height_m = height / 100
    bmi = round(weight / (height_m ** 2), 2)

    if bmi < 18.5:
        category = "Niedowaga"
    elif bmi < 25:
        category = "Prawidłowa"
    elif bmi < 30:
        category = "Nadwaga"
    else:
        category = "Otyłość"

    return JsonResponse({
        "bmi": bmi,
        "category": category
    })


# 🔥 AJAX KALORIE
def calculate_calories(request):
    data = json.loads(request.body)

    weight = float(data.get("weight"))
    goal = data.get("goal")

    base = weight * 24

    if goal == "lose":
        calories = int(base - 300)
    elif goal == "maintain":
        calories = int(base)
    else:
        calories = int(base + 300)

    return JsonResponse({
        "calories": calories
    })


@login_required
def saved_posts(request):
    saved_posts = request.user.saved_posts.all()
    return render(request, "main/recipes.html", {"saved_posts": saved_posts})


def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, "main/user_profile.html", {"profile_user": user})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'main/detail.html', {'post': post})
>>>>>>> Stashed changes
