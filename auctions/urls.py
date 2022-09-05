from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),                #if the path is this then index function in views.py is called
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.newlisting, name="newlisting"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category_name>", views.category_each, name="category_each"),
    path("to_watchlist/<int:listing_id>", views.to_watchlist, name="to_watchlist"),
    path("remove_watchlist/<int:listing_id>", views.remove_watchlist, name="remove_watchlist"),
    path("close_listing/<int:listing_id>", views.close_listing, name="close_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),        # <str:title_id> expect to receive a str as a variable    
]
