from pickle import TRUE
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

#superuser admin, admin@example.com, 123@admn

class User(AbstractUser):
    pass
    def __str__(self):
        return f"{self.username} (ID:{self.id})"       #string representation for an object

class Listing(models.Model):
    title = models.CharField(max_length=128)    #Charfield needs a max value
    description = models.TextField()                #TextField does not need a max value
    category = models.CharField(max_length=64)
    img_url = models.URLField(max_length=512)
    starting_bid = models.IntegerField()
    bid_number = models.IntegerField()
    current_price = models.IntegerField()
    created_at = models.DateTimeField(default = timezone.now, blank=False)      #auto date and time when the object is created
    active_state = models.BooleanField(default=True)       #True/False
    user = models.ForeignKey(User, on_delete=models.CASCADE)        #one to many realaionship - for one User(one raw) there can be many Listing(many raws)- one User can be there in in several rows
    #on_delete=models.CASCADE - if parent(User) deleted all the childs(Listing) will be deleted
    
    def __str__(self):
        return f"{self.title} (ID:{self.id})"   

    
class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)         #one to one - for one Watchlist only one User and wise versa - one User can not be there in another row
    listings = models.ManyToManyField(Listing, blank=True)     #many to many - for one Listing there can be many Watchlists and for one Watchlist therecan be many Listing

    def __str__(self):
        return f"Watchlist of {self.user} (ID:{self.user.id})"
    

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)        #one bid can have only one users but a user can have multiple bids
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)      #one bid can be in only one listing but a listing can have multiple bids
    value = models.IntegerField(default="0")
    bid_time = models.DateTimeField(default = timezone.now, blank=False)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)
    comment = models.TextField(null=True)




