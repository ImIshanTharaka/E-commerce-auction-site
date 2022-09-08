# E-commerce-auction-site

An e-commerce auction site where users can log into their accounts, post new auction listings, place bids on listings, comment on listings, and add listings to their “watchlist”. Users can close their listings and the highest bidder wins the auction.

# Specifications
* Useers: Users who are registered on the site can log in using their usernames and passwords, and they can logout at anytime they want.
* Create Listing: Users able to visit a page to create a new listing. They can specify a title for the listing, a text-based description, and what the starting bid should be. Users can optionally provide a URL for an image for the listing and/or assign a category to the listing.
* Active Listings Page: The default route of your web application let users view all of the currently active auction listings. For each active listing, this page displays the title, description, current price, and photo.
* Listing Page: Clicking on a listing should takes users to a page specific to that listing. On that page, users able to view all details about the listing, including the current price for the listing.
  * If the user is signed in, the user can add the item to their “Watchlist.” If the item is already on the watchlist, the user can remove it.
  * If the user is signed in, the user can bid on the item.
  * If the user is signed in and is the one who created the listing, the user have the ability to “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
  * If a user is signed in on a closed listing page, and the user has won that auction, the page says so.
  * Users who are signed in can add comments to the listing page.
* Watchlist: Users who are signed in able to visit a Watchlist page, which displays all of the listings that a user has added to their watchlist. Clicking on any of those listings takes the user to that listing’s page.
* Categories: Users able to visit a page that displays a list of all listing categories. Clicking on the name of any category takes the user to a page that displays all of the active listings in that category.

# What I learned
* Working with Django models
* SQlite database management with Django
* Obtain user inputs with Djnago forms and manupulate the database accordingly
* Managing user accounts, logins and logouts
* Using Django admin interface
* Working with Django HTML templates

