from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from difflib import get_close_matches
import unicodedata
import re
import json

from forum.models import Post
from .models import Recipe


def index(request):
    return render(request, 'main/index.html')

def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        # 🔥 LIMITY
        if len(username) > 150:
            messages.error(request, "Za długa nazwa użytkownika")
            return redirect('login_user')

        if len(password) > 128:
            messages.error(request, "Hasło za długie")
            return redirect('login_user')

        user = authenticate(
            username=username,
            password=password
        )

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
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        # 🔥 LIMITY
        if len(username) > 150:
            messages.error(request, "Nazwa użytkownika za długa")
            return render(request, 'main/users/register.html')

        if len(email) > 254:
            messages.error(request, "Email za długi")
            return render(request, 'main/users/register.html')

        if len(password) > 128:
            messages.error(request, "Hasło za długie")
            return render(request, 'main/users/register.html')

        if not email:
            messages.error(request, "Email jest wymagany")
            return render(request, 'main/users/register.html', {
                'username': username,
                'email': email
            })

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.error(request, "Podaj poprawny adres email")
            return render(request, 'main/users/register.html', {
                'username': username,
                'email': email
            })

        if User.objects.filter(email=email).exists():
            messages.error(request, "Użytkownik o tym emailu już istnieje")
            return render(request, 'main/users/register.html', {
                'username': username,
                'email': email
            })

        if User.objects.filter(username=username).exists():
            messages.error(request, "Taka nazwa użytkownika już istnieje")
            return render(request, 'main/users/register.html', {
                'username': username,
                'email': email
            })

        if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[0-9]', password):
            messages.error(request, "Hasło musi mieć min. 8 znaków, dużą literę i cyfrę")
            return render(request, 'main/users/register.html', {
                'username': username,
                'email': email
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        return redirect('home')

    return render(request, 'main/users/register.html')


def logout_user(request):
    logout(request)
    return redirect('home')


def normalize_text(text):
    text = text.lower().strip()
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    return text


def recipes(request):
    query = request.GET.get("q", "").strip()

    if len(query) > 100:
        query = query[:100]

    results = []
    favorite_ids = []
    favorite_recipes = []

    if query:
        results = Recipe.objects.all()

        normal_results = results.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(ingredients__icontains=query)
        ).distinct()

        if normal_results.exists():
            results = normal_results
        else:
            all_recipes = Recipe.objects.all()

            title_map = {}
            for recipe in all_recipes:
                normalized_title = normalize_text(recipe.title)
                title_map[normalized_title] = recipe.id

            close_titles = get_close_matches(
                normalize_text(query),
                title_map.keys(),
                n=10,
                cutoff=0.6
            )

            matched_ids = [title_map[title] for title in close_titles]
            results = Recipe.objects.filter(id__in=matched_ids)

    if request.user.is_authenticated:
        favorite_ids = request.user.favorite_recipes.values_list('id', flat=True)
        favorite_recipes = request.user.favorite_recipes.select_related()
        forum_post_ids = [recipe.forum_post_id for recipe in favorite_recipes if recipe.forum_post_id]
        forum_posts_map = {post.id: post for post in Post.objects.filter(id__in=forum_post_ids)}
        saved_posts = request.user.saved_posts.all()
    else:
        saved_posts = None
        forum_posts_map = {}

    return render(request, "main/recipes.html", {
        "query": query,
        "results": results,
        "favorite_ids": favorite_ids,
        "favorite_recipes": favorite_recipes,
        "saved_posts": saved_posts,
        "forum_posts_map": forum_posts_map,
    })


def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'main/detail.html', {'recipe': recipe})


@login_required
def toggle_favorite(request, id):
    recipe = get_object_or_404(Recipe, id=id)

    if recipe.forum_post_id and request.user.saved_posts.filter(id=recipe.forum_post_id).exists():
        messages.error(request, 'Ten przepis masz już zapisany w sekcji „Zapisane posty z forum”.')
        return redirect('recipes')

    if request.user in recipe.favorites.all():
        recipe.favorites.remove(request.user)
    else:
        recipe.favorites.add(request.user)

    return redirect(request.META.get('HTTP_REFERER', 'recipes'))


def health(request):
    return render(request, "main/health.html")


def calculate_bmi(request):
    if request.method == "POST":
        data = json.loads(request.body)

        height = float(data.get("height", 0))
        weight = float(data.get("weight", 0))

        if height < 100 or height > 250 or weight < 30 or weight > 300:
            return JsonResponse({"error": "Invalid data"})

        if height == 0:
            return JsonResponse({"error": "Invalid data"})

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


def calculate_calories(request):
    if request.method == "POST":
        data = json.loads(request.body)

        weight = float(data.get("weight", 0))

        if weight < 30 or weight > 300:
            return JsonResponse({"error": "Invalid data"})

        goal = data.get("goal")

        base = weight * 24

        if goal == "lose":
            calories = int(base - 300)
        elif goal == "maintain":
            calories = int(base)
        elif goal == "gain":
            calories = int(base + 300)
        else:
            calories = 0

        return JsonResponse({
            "calories": calories
        })


@login_required
def saved_posts(request):
    saved_posts = request.user.saved_posts.all()

    return render(request, "main/recipes.html", {
        "saved_posts": saved_posts
    })


def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, "main/user_profile.html", {
        "profile_user": user
    })


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)

    return render(request, 'main/detail.html', {
        'post': post
    })