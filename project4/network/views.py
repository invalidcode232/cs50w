from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    # if request method is post, add a Post to the database
    if request.method == "POST":
        if "follow" in request.POST:
            Follower.objects.create(user=request.user, following=user)
        elif "unfollow" in request.POST:
            Follower.objects.filter(user=request.user, following=user).delete()
        elif "like" in request.POST:
            # Add like in post
            post_id = request.POST["post_id"]
            post = Post.objects.get(id=post_id)

            if post.user != request.user:
                post.like.add(request.user)
                post.save()
        elif "unlike" in request.POST:
            # Remove like in post
            post_id = request.POST["post_id"]
            post = Post.objects.get(id=post_id)

            if post.user != request.user:
                post.like.remove(request.user)
                post.save()
        elif "edit" in request.POST:
            # Edit post
            post_id = request.POST["post_id"]
            post = Post.objects.get(id=post_id)

            if post.user == request.user:
                post.content = request.POST["content"]
                post.save()
        else:
            # get the post data from the form
            content = request.POST["content"]
            # create a new post object
            new_post = Post(content=content, user=request.user)
            # save the post object to the database
            new_post.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        # get all posts from the database and pass them to the template sorted by date descending
        posts = Post.objects.order_by("-created_at")

        # paginate the posts to show only 10 posts per page
        paginator = Paginator(posts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "network/index.html", {
            "page_obj": page_obj
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request, profile_id):
    if request.method == "POST":
        # If user is logged, follow and unfollow the profile
        user = User.objects.get(id=profile_id)

        if request.user.is_authenticated:
            if "follow" in request.POST:
                Follower.objects.create(user=request.user, following=user)
            elif "unfollow" in request.POST:
                Follower.objects.filter(user=request.user, following=user).delete()
            elif "like" in request.POST:
                # Add like in post
                post_id = request.POST["post_id"]
                post = Post.objects.get(id=post_id)

                if post.user != request.user:
                    post.like.add(request.user)
                    post.save()
            elif "unlike" in request.POST:
                # Remove like in post
                post_id = request.POST["post_id"]
                post = Post.objects.get(id=post_id)

                if post.user != request.user:
                    post.like.remove(request.user)
                    post.save()
            elif "edit" in request.POST:
                # Edit post
                post_id = request.POST["post_id"]
                post = Post.objects.get(id=post_id)

                if post.user == request.user:
                    post.content = request.POST["content"]
                    post.save()

        return HttpResponseRedirect(reverse("profile", args=[profile_id]))
    else:
        # get the user object
        profile_user = User.objects.get(id=profile_id)
        # get all posts from the database and pass them to the template sorted by date descending
        posts = Post.objects.filter(user=profile_user).order_by("-created_at")

        # paginate the posts to show only 10 posts per page
        paginator = Paginator(posts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # Get user following count using the Follower class
        following_count = Follower.objects.filter(user=profile_user).count()
        # Get user follower count using the Follower class
        follower_count = Follower.objects.filter(following=profile_user).count()

        # Get if the current user is following the profile user
        is_logged_in = request.user.is_authenticated
        is_current_user = request.user == profile_user
        is_following = is_logged_in and Follower.objects.filter(user=request.user, following=profile_user).exists()

        return render(request, "network/profile.html", {
            "profile_user": profile_user,
            "posts": posts,
            "following_count": following_count,
            "followers_count": follower_count,
            "is_logged_in": is_logged_in,
            "is_current_user": is_current_user,
            "is_following": is_following,
            "page_obj": page_obj
        })


# Only shows the posts of the users that the current user is following
@login_required
def following(request):
    # Get the current user's following list
    following_list = Follower.objects.filter(user=request.user)
    # Convert following_list to a list of users
    following_list = [follower.following for follower in following_list]
    # Get all posts from the database and pass them to the template sorted by date descending
    posts = Post.objects.filter(user__in=following_list).order_by("-created_at")

    # paginate the posts to show only 10 posts per page
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "page_obj": page_obj
    })