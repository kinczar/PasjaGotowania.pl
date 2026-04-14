from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from forum.models import Post
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

@login_required
def profile(request, user_id=None):

    if user_id:
        profile_user = get_object_or_404(User, id=user_id)
    else:
        profile_user = request.user

    user_posts_count = Post.objects.filter(author=profile_user).count()

    context = {
        'profile_user': profile_user,
        'user_posts_count': user_posts_count,
    }

    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            if request.POST.get('remove_picture'):
                request.user.profile.profile_picture = None
                request.user.profile.save()

            user_form.save()
            profile_form.save()
            messages.success(request, "Profil został zaktualizowany!")
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Hasło zostało zmienione!")
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})


def user_profile(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)

    user_posts_count = Post.objects.filter(author=user_obj).count()

    return render(request, 'accounts/profile.html', {
        'profile_user': user_obj,
        'user_posts_count': user_posts_count,
    })