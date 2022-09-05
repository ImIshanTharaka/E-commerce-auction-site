from audioop import add
from typing_extensions import Self
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.contrib import messages     #massages module for displaying massages

from .models import *           #from models.py import all
from django import forms        #for djago forms
from django.db.models import Max        #to get maximum value of a field


"""
Index page
"""
def index(request):
    listing_list=Listing.objects.filter(active_state=True)      #get all th objects of Listing model
    return render(request, "auctions/index.html", {
        "listing_list":listing_list
    })


"""
Login page
"""
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)      #check if the username & password are correct

        # Check if authentication successful
        if user is not None:
            login(request, user)    #log user in
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


"""
Logout
"""
def logout_view(request):
    logout(request)     #log user out
    return HttpResponseRedirect(reverse("index"))       #goes to 'logout' url and redirect to 'index' url


"""
Resister page
"""
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


'''
required forms
'''

#django form for commenting
class comment_form(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'style': 'height: 70px', 'class': 'form-control'}), label="Comment :")

#django form for bidding
class bid_form(forms.Form):               
    bid = forms.IntegerField(widget=forms.TextInput(attrs={'style': 'width: 200px;', 'class': 'form-control'}),label="Bid ($) :")

category =  [
    ('','No Category Listed'),
    ('fashion', 'Fashion'),
    ('electronics', 'Electronics'),
    ('health & beauty', 'Health & Beauty'),
    ('home & garden', 'Home & Garden'),
    ('sports','Sports'),
    ('collectibles and art','Collectibles and Art'),
    ('industrial equipment','Industrial Equipment'),
    ]

#django form for newlisting
class new_listing_form(forms.Form):               
    title = forms.CharField(widget=forms.TextInput(attrs={'style': 'width: 400px;', 'class': 'form-control'}), label="Title")
    category = forms.ChoiceField(choices=category, required=False, widget=forms.Select(attrs={'style': 'width: 200px;','class': 'form-control'}),label="Category")
    description = forms.CharField(widget=forms.Textarea(attrs={'style': 'height: 300px', 'class': 'form-control'}), label="Description")
    img_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'style': 'width: 800px;', 'class': 'form-control'}), label="URL for an image")
    starting_bid = forms.IntegerField(widget=forms.TextInput(attrs={'style': 'width: 200px;', 'class': 'form-control'}), label="Starting Bid ($)")


"""
New Listing adding page
"""

def newlisting(request):
    if request.method == "POST":         #if post new listing
        form = new_listing_form(request.POST)
        if form.is_valid():
            title =  str(form.cleaned_data["title"]).capitalize()
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            img_url = form.cleaned_data["img_url"]
            category = form.cleaned_data["category"]
            listing=Listing.objects.create(               #creating an object
                title=title,
                description=description,
                starting_bid=starting_bid,
                img_url=img_url,
                category=category,
                bid_number=0,
                current_price=starting_bid,
                user= request.user
                )                                   
            listing.save()                          #saving the object to the database
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "bid_form":bid_form(),
                "watchlist_button": False,
                "comment_form" : comment_form(),
                "comments" : Comment.objects.filter(listing=listing).all()
            })
        else:
            return render (request, "auctions/newlisting.html",{       #form back to the user with input form data
                "form":form})
    return render (request, "auctions/newlisting.html",{       #before adding a new listing
        "form":new_listing_form(),                         #returns empty form
    })



"""
Listing page
"""

def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    
    #for watchlist button
    if request.user.is_authenticated:
        # if the item already exists in that user watchlist then TRUE
        watchlist_button = Watchlist.objects.filter(user=request.user, listings=listing_id).exists()
    else:
        watchlist_button = False
        
    #deactivate a listing and inform the winner
    if listing.active_state == False:
        winner = Bid.objects.filter(listing=listing).latest("bid_time").user      # user of the latest bids of this list
        if winner == request.user:
            messages.success(request, "Congratulations..! You have won this Bid!")

    #for commenting
    if "comment_form" in request.POST:
        form = comment_form(request.POST)
        if form.is_valid():
            comment =  form.cleaned_data["comment"]         # "comment" is the object inside the bid_form
            Comment.objects.create(user=request.user, listing=listing, comment=comment)
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    #for bidding
    if "bid_form" in request.POST:
        form = bid_form(request.POST)
        if form.is_valid():
            bid =  form.cleaned_data["bid"]     # "bid" is the object inside the bid_form
            if listing.bid_number == 0 and bid >= listing.starting_bid:
                listing.bid_number+=1
                listing.current_price = bid
                Bid.objects.create(user=request.user, listing=listing, value=listing.current_price)
                messages.success(request, "Successfully Bid!")
            elif listing.bid_number != 0 and bid > listing.current_price:
                listing.bid_number+=1
                listing.current_price = bid
                Bid.objects.create(user=request.user, listing=listing, value=listing.current_price)
                messages.success(request, "Successfully Bid!")
            else:
                messages.error(request, "Invalid Bid!")
            listing.save()          # after updating a object save it
            return HttpResponseRedirect(reverse("listing", args=(listing_id,))) 
    
    return render(request, "auctions/listing.html", {
                "listing": listing,
                "bid_form":bid_form(),
                "watchlist_button": watchlist_button,
                "comment_form" : comment_form(),
                "comments" : Comment.objects.filter(listing=listing).all()
            })


'''
adding/remove listing from watchlist
'''
def to_watchlist(request, listing_id):
    listing = Listing.objects.get(id=listing_id)     
    user_list, created = Watchlist.objects.get_or_create(user=request.user)     # Get the user watchlist or create it if it doesn't exists 
    #user_list is the object created from Watchlist considering user
    user_list.listings.add(listing)                                         # Add the item through the ManyToManyField which is listings (user is the one to one field)
    messages.success(request, "Successfully added to your watchlist")
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))     

def remove_watchlist(request, listing_id):
    user_list = Watchlist.objects.get(user=request.user)        #get the Watchlist item
    listing = Listing.objects.get(id=listing_id)             #get the listing
    user_list.listings.remove(listing)                   #add the listing to the listings attribute of the Watchlist   
    messages.success(request, "Successfully removed from your watchlist")
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))  



'''
watchlist page
'''    
def watchlist(request):
    user_list,create = Watchlist.objects.get_or_create(user=request.user) 
    if user_list.listings == None: 
        return render(request, "auctions/watchlist.html",{
            "user_list": False,
            })
    else:
        return render(request, "auctions/watchlist.html",{
            "user_list": user_list.listings.all(),
            })


'''
close listing
'''
def close_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.active_state = False
    listing.save()
    return HttpResponseRedirect(reverse("index"))


'''
categories page
'''   
def categories(request):
    category_items = []
    for item in category[1:]:
        category_items.append(item[1])
    return render(request, "auctions/categories.html",{
            "categories": category_items,
            })

'''
for each category page
'''
def category_each(request,category_name):
    category_listings = Listing.objects.filter(category=category_name.lower()).all()
    return render(request, "auctions/category_each.html",{
            "category_name" : category_name,
            "categories": category_listings
            })


        




