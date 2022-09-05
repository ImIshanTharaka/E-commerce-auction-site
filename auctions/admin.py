from django.contrib import admin
from .models import *    #importing models

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "category", "starting_bid", "current_price")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    filter_horizontal = ("listings",)   #nice representation for M-M relationships in admin interface

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "listing", "value")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "listing", "comment")

admin.site.register(User,UserAdmin)   #registring models in admin app-admin app can be used to add/modify data in the model
admin.site.register(Listing, ListingAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)