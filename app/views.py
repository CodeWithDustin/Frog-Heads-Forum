### library imports ###
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
from itertools import chain
from django.urls import reverse
from itertools import chain

### imports from other files in our project ###
from app.models import *
from app.forms import *


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

            #make a profile for the user
            profile = Profile.objects.create(username=user)
            profile.save()


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
# def create_profile_view(request):


#     # profile = get_object_or_404(Profile, pk=)

#     # if n

#     # form = ProfileForm()

#     if request.method == 'POST':
#         form = ProfileForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return render(request, 'profile.html')

    
#     context = {
#         'form' : form,
#     }

#     return render(request, 'edit_profile.html', context)


# user can see account details, and post history
def profile_view(request):
    
    user = request.user
    profile = Profile.objects.get(username=user)
    all_posts = Post.objects.filter(user=user)
    all_replies = Reply.objects.filter(user=user)

    all_posts_and_replies = list(chain(all_posts, all_replies))

    # we could do something like ↓ to get the profile directly
    # user_profile = Profile.objects.get(username = request.user)

    context = {
        'user' : user,
        'profile' : profile,
        'all_posts' : all_posts_and_replies,
    }

    return render(request, 'profile.html', context)


# user can edit account details (username, pfp, etc.)
def edit_profile_view(request, profile_id: int):
    
    profile = Profile.objects.get(id=profile_id)
    user = request.user


    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return render(request, 'profile.html')

    context = {
        'form' : form,
        'user' : user,
    }

    return render(request, 'edit_profile.html', context)


# user can see all posts in a selected forum category, make a post in that category, and upvote/downvote posts
# login optional, but required to make a post or upvote/downvote
# moderator can delete posts
def forum_view(request, board_id: int):

    form = PostForm()
    
    board = MessageBoard.objects.get(id=board_id)

    posts = Post.objects.filter(board=board)

    is_moderator = request.user.groups.filter(name="Moderator").exists()


    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            post.user = request.user
            post.board = board

            post.save()

            return redirect('forum', board_id=board.id)


    context = {
        'board' : board,
        'posts' : posts,
        'form' : form,
        'is_moderator': is_moderator,
    }

    return render(request, 'forum.html', context)


# user can make a post in a selected forum category, login required
@login_required(login_url='login')
def create_post_view(request, board_id: int):
    
    
    board = MessageBoard.objects.get(id=board_id)

    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)

            post.user = request.user
            post.board = board

            post.save()

            return redirect('forum', board_id=board.id)
        
    context = {
        'form' : form,
    }

    return render(request, 'create_post.html', context)

@login_required
def edit_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Check if the logged in user is the owner of the post
    if request.user != post.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('forum', board_id=post.board.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'edit_post.html', {'form': form, 'post': post})


@login_required
def reply_to_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = post
            reply.user = request.user
            reply.save()
            return redirect('forum', board_id=post.board.id)  # Redirect to the forum or post page
    else:
        form = ReplyForm()
    
    return render(request, 'reply.html', {'form': form, 'post': post})

@login_required
def delete_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    post = reply.post
    if request.user == reply.user or request.user.groups.filter(name='Moderator').exists():
        reply.delete()
    return redirect('forum', board_id=post.board.id)

def load_more_replies(request, post_id):
    replies = Reply.objects.filter(post_id=post_id)[3:6]  # Fetch replies 4 to 6
    has_more_replies = True if Reply.objects.filter(post_id=post_id).count() > 6 else False

    data = {
        'replies': [
            {
                'user': {
                    'profile': {
                        'profile_img': reply.user.profile.profile_img.url
                    },
                    'username': reply.user.username
                },
                'date_replied': reply.date_replied,
                'reply': reply.reply
            }
            for reply in replies
        ],
        'has_more_replies': has_more_replies
    }
    return JsonResponse(data)


### Moderator Only Views ###


# moderator category control panel
def board_control_view(request):

    # check if user is in moderator group
    if not request.user.groups.filter(name='Moderator').exists():
        return HttpResponse('You are not authorized to view this page')



    form = BoardForm()

    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('board_control')



    context = {
        'all_boards' : MessageBoard.objects.all(),
        'form' : form,
    }

    return render(request, 'moderator_panel.html', context)


# moderator can create a new forum category
def create_board_view(request):

    form = BoardForm()

    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('board_control')
        
    context = {
        'form' : form,
    }

    return render(request, 'create_board.html', context)


# moderator can delete a forum category
def delete_board_view(request, board_id: int):
    
    board = MessageBoard.objects.get(id=board_id)
    board.delete()

    return redirect('board_control')


# moderator can update a forum category, such as rename / change description
def update_board_view(request, board_id: int):

    board = MessageBoard.objects.get(id=board_id)

    form = BoardForm(instance=board)

    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            return redirect('board_control')

    # gonna need a form here 

    context = {
        'form' : form,
    }

    return render(request, 'update_board.html', context)

# moderator can delete a post
def delete_post_view(request, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    
    # Check if the request user is the post owner or a moderator
    if request.user == post.user or request.user.groups.filter(name='Moderator').exists():
        post.delete()
        return redirect('forum', board_id=post.board.id)
    else:
        return HttpResponseForbidden("You are not allowed to delete this post.")


@login_required
def edit_perms_view(request):
    query = request.GET.get('q')
    moderator_group = Group.objects.get(name='Moderator')

    if query:
        all_users = User.objects.filter(username__icontains=query)
    else:
        all_users = User.objects.filter(groups=moderator_group)

    context = {
        'all_users': all_users,
    }
    return render(request, 'edit_perms.html', context)


@login_required
def toggle_perms_view(request, user_id):
    user = User.objects.get(id=user_id)
    moderator_group = Group.objects.get(name='Moderator')
    
    if moderator_group in user.groups.all():
        user.groups.remove(moderator_group)
    else:
        user.groups.add(moderator_group)
    
    return redirect('edit_perms')


def search(request):
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(username__icontains=query)
        profiles = Profile.objects.filter(username__in=users)
    else:
        profiles = []

    return render(request, 'search.html', {"profiles":profiles})
    
def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    all_posts = Post.objects.filter(user=user)
    all_replies = Reply.objects.filter(user=user)
    all_posts_and_replies = list(chain(all_posts, all_replies))


    return render(request, 'profile_detail.html', {'profile_user': user, 'profile':profile, 'all_posts':all_posts_and_replies})