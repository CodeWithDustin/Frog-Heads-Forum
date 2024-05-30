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

    return render(request, "login.html", context)


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

    return render(request, "registration.html", context)


# user logout
def logout_view(request):
    logout(request)
    return redirect("home")


# user can see all forum categories, click on one to see all posts in that category
# moderator could create/update/delete categories
def home_view(request):

    all_boards = MessageBoard.objects.all()


    

    context = {
        'all_boards' : all_boards,
    }

    return render(request, "home.html", context)


# user can create profile, login required
def create_profile_view(request):
    pass


# user can see account details, and post history
def profile_view(request):
    
    user = request.user


    # we could do something like ↓ to get the profile directly
    user_profile = Profile.objects.get(username = request.user)

    context = {
        'user' : user,
    }

    return render(request, 'profile.html', context)


# user can edit account details (username, pfp, etc.)
def edit_profile_view(request):
    pass


# user can see all posts in a selected forum category, make a post in that category, and upvote/downvote posts
# login optional, but required to make a post or upvote/downvote
# moderator can delete posts
def forum_view(request, board_id: int):
    
    board = MessageBoard.objects.get(id=board_id)

    posts = Post.objects.filter(board=board)

    context = {
        'board' : board,
        'posts' : posts,
    }

    return render(request, 'need a file', context)


# user can make a post in a selected forum category, login required
def create_post_view(request, board_id: int):
    pass


### Moderator Only Views ###


# moderator category control panel
def board_control_view(request):


    
    return render(request, 'need html file')


# moderator can create a new forum category
def create_board_view(request):
    pass


# moderator can delete a forum category
def delete_board_view(request, board_id: int):
    
    board = MessageBoard.objects.get(id=board_id)
    board.delete()

    return redirect('board_control')


# moderator can update a forum category, such as rename / change description
def update_board_view(request, board_id: int):

    board = MessageBoard.objects.get(id=board_id)

    # gonna need a form here 

    pass


# moderator can delete a post
def delete_post_view(request, post_id: int):
    
    post = Post.objects.get(id=post_id)
