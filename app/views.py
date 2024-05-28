### library imports ###
from django.shortcuts import render


### imports from other files in our project ###


### Regular User Views ###


# user login
def login_view(request):
    pass


# register user with Django's default user model
def register_view(request):
    pass


# user logout
def logout_view(request):
    pass


# user can see all forum categories, click on one to see all posts in that category
# moderator could create/update/delete categories
def home_view(request):
    pass


# user can see account details, and post history
def profile_view(request):
    pass


# user can edit account details (username, pfp, etc.)
def edit_profile_view(request):
    pass


# user can see all posts in a selected forum category, make a post in that category, and upvote/downvote posts
# login optional, but required to make a post or upvote/downvote
# moderator can delete posts
def forum_view(request):
    pass


# user can make a post in a selected forum category, login required
def create_post_view(request):
    pass


### Moderator Only Views ###


# moderator can create a new forum category
def create_category_view(request):
    pass


# moderator can delete a forum category
def delete_category_view(request):
    pass


# moderator can update a forum category
def update_category_view(request):
    pass


# moderator can delete a post
def delete_post_view(request):
    pass
