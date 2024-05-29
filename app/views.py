### library imports ###
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

### imports from other files in our project ###
from app.models import Profile, MessageBoard, Post
from app.forms import LoginForm


### Regular User Views ###


# user login
def login_view(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # user will be none if authentication fails
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                ## add error message here ##
                pass

    context = {
        "form": form,
    }

    return render(request, "template name", context)


# register user with Django's default user model
def register_view(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            ## add user to group (need to create group in admin panel)##
            user.save()
            return redirect("login")

    context = {
        "form": form,
    }

    return render(request, "template name", context)


# user logout
def logout_view(request):
    logout(request)
    return redirect("home")


# user can see all forum categories, click on one to see all posts in that category
# moderator could create/update/delete categories
def home_view(request):
    return render(request, "home.html")


# user can create profile, login required
def create_profile_view(request):
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
