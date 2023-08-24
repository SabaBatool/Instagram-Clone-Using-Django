from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from userauths.forms import UserRegisterForm


from polls.models import Post, Follow, Stream
from django.contrib.auth.models import User
from userauths.models import Profile

# from .forms import EditProfileForm, UserRegisterForm
from django.urls import resolve

# from comment.models import Comment


def UserProfile(request, username):
    Profile.objects.get_or_create(user=request.user)
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name
    posts = Post.objects.filter(user=user).order_by("-posted")

    if url_name == "profile":
        posts = Post.objects.filter(user=user).order_by("-posted")
    else:
        posts = profile.favourite.all()

    # Profile Stats
    posts_count = Post.objects.filter(user=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    followers_count = Follow.objects.filter(following=user).count()
    # count_comment = Comment.objects.filter(post=posts).count()
    follow_status = Follow.objects.filter(
        following=user, follower=request.user
    ).exists()

    # pagination
    paginator = Paginator(posts, 8)
    page_number = request.GET.get("page")
    posts_paginator = paginator.get_page(page_number)

    context = {
        "posts": posts,
        "profile": profile,
        "posts_count": posts_count,
        "following_count": following_count,
        "followers_count": followers_count,
        "posts_paginator": posts_paginator,
        "follow_status": follow_status,
        # 'count_comment':count_comment,
    }
    return render(request, "userauths/profile.html", context)


def follow(request, username, option):
    user = request.user
    following = get_object_or_404(User, username=username)

    try:
        f, created = Follow.objects.get_or_create(
            follower=request.user, following=following
        )

        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=following, user=request.user).all().delete()
        else:
            posts = Post.objects.all().filter(user=following)[:25]
            with transaction.atomic():
                for post in posts:
                    stream = Stream(
                        post=post,
                        user=request.user,
                        date=post.posted,
                        following=following,
                    )
                    stream.save()
        return HttpResponseRedirect(reverse("profile", args=[username]))

    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("profile", args=[username]))


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            # Profile.get_or_create(user=request.user)
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hurray your account was created!!")

            # Automatically Log In The User
            new_user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
            )
            login(request, new_user)
            # return redirect('editprofile')
            return redirect("index")

    elif request.user.is_authenticated:
        return redirect("index")
    else:
        form = UserRegisterForm()
    context = {
        "form": form,
    }
    return render(request, "polls/sign-up.html", context)
