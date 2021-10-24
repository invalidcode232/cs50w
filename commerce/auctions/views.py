from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

import auctions.models
from .models import *


def index(request):
    listings = Listing.objects.all()

    return render(request, "auctions/index.html", {
        "name": "Active Listings",
        "listings": listings,
        "count": listings.count()
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create(request):
    if request.method == "GET":
        categories = Category.objects.all()

        return render(request, "auctions/create.html", {
            "categories": categories
        })
    elif request.method == "POST":
        user = request.user
        name = request.POST["name"]
        description = request.POST["desc"]
        image_url = request.POST["image_url"]
        price = request.POST["price"]
        category_id = request.POST["category"]

        listing = Listing(user=user, name=name, description=description, image_url=image_url, price=price)
        listing.save()
        category = Category.objects.get(id=category_id)
        listing.category.add(category)

        return HttpResponseRedirect(reverse("index"))


def view_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    is_owner = listing.user == request.user
    is_winner = not listing.is_open and listing.user

    return render(request, "auctions/view.html", {
        "listing": listing,
        "is_owner": is_owner,
        "is_winner": is_winner
    })


@login_required
def watchlist(request):
    if request.method == "GET":
        watchlist_listings = request.user.watchlist_listings.all()

        return render(request, "auctions/watchlist.html", {
            "listings": watchlist_listings
        })
    elif request.method == "POST":
        listing_id = request.POST["listing_id"]

        listing = Listing.objects.get(pk=listing_id)
        listing.watchlist_users.add(request.user)

        return HttpResponseRedirect(reverse("watchlist"))


@login_required
def bid_listing(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        bid = int(request.POST["bid"])

        listing = Listing.objects.get(pk=listing_id)

        if bid > listing.price:
            listing.bids += 1
            listing.bidder = request.user
            listing.price = bid
            listing.save()

        return HttpResponseRedirect(reverse("index"))


def close_listing(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]

        listing = Listing.objects.get(pk=listing_id)
        listing.is_open = False
        listing.save()

        return HttpResponseRedirect(reverse("index"))


def view_categories(request):
    categories = Category.objects.all()

    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def view_category(request, category_id):
    category = Category.objects.get(id=category_id)
    category_listings = category.category_listings.all()

    return render(request, "auctions/index.html", {
        "name": f"Active listing: {category.name}",
        "listings": category_listings,
        "count": category_listings.count()
    })

