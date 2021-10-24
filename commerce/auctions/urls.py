from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("close", views.close_listing, name="close"),
    path("bid", views.bid_listing, name="bid"),
    path("categories", views.view_categories, name="categories"),
    path("categories/<int:category_id>", views.view_category, name="category"),
    path("<int:listing_id>", views.view_listing, name="listing")
]
