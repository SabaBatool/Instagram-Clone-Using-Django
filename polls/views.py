from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from polls.models import Post, Tag, Stream, Likes
from polls.forms import NewPostform
from userauths.models import Profile


def index(request):
    user = request.user
    user = request.user
    posts = Stream.objects.filter(user=user)
    group_ids = []
    for post in posts:
        group_ids.append(post.post_id)
    post_items = Post.objects.filter(id__in=group_ids).all().order_by("-posted")
    context = {
        "post_items": post_items,
    }
    return render(request, "polls/index.html", context)


def NewPost(request):
    user = request.user.id
    tags_objs = []
    if request.method == "POST":
        form = NewPostform(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get("picture")
            caption = form.cleaned_data.get("caption")
            tag_form = form.cleaned_data.get("tag")
            # tags_list = list(tag_form.split(","))

            # for tag in tags_list:
            #     t, created = Tag.objects.get_or_create(title=tag)
            #     tags_objs.append(t)
            p, created = Post.objects.get_or_create(
                picture=picture, caption=caption, user_id=user
            )
            p.tags.set(tags_objs)
            p.save()
            return redirect("index")
    else:
        form = NewPostform()
    context = {"form": form}
    return render(request, "polls/newpost.html", context)


def PostDetail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {
        "post": post,
    }
    return render(request, "polls/post-details.html", context)


def Tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by("-posted")

    context = {"posts": posts, "tag": tag}
    return render(request, "polls/tag.html", context)


def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()

    if not liked:
        Likes.objects.create(user=user, post=post)
        current_likes = current_likes + 1
    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1

    post.likes = current_likes
    post.save()
    # return HttpResponseRedirect(reverse('post-details', args=[post_id]))
    return HttpResponseRedirect(reverse("post-details", args=[post_id]))


def favourite(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)

    if profile.favourite.filter(id=post_id).exists():
        profile.favourite.remove(post)
    else:
        profile.favourite.add(post)
    return HttpResponseRedirect(reverse("polls/post-details", args=[post_id]))
