from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse,resolve
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Sum
from datetime import datetime, timedelta
from django.conf import settings
from django.core.paginator import Paginator
from .models import *
from .forms import *
import json
from django.db import transaction
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


# def home(request):
#     return render(request,'home.html')


def webpage(request):
    return render(request,'web.html')


def tweetfeed(request):
    user = request.user
    tweetitems = Tweet.objects.all().order_by('-created')
    profile = Profile.objects.all()
    context = {
        'tweetitems': tweetitems,
        'profile': profile,
    }
    return render(request, 'tweetfeed.html', context)


def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            profile=Profile.objects.get(user=request.user)
            profile.status=True
            profile.save()
            screen_time = ScreenTime.objects.create(user=user,login_time = timezone.now())
            return redirect(feed)
        else:
            messages.error(request, "Bad Credentials !")
    storage = messages.get_messages(request)
    storage.used = True
    return render(request, 'signin.html')



def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        pass1 = request.POST['pass1']
        myuser = User.objects.create_user(username,email,pass1)
        
        #Emailing Users
        host_email=settings.EMAIL_HOST_USER
        sender_mail=myuser.email
        subject="Welcome to Hash"
        message="Hello, "+myuser.username+" looking forward to seeing you around, Have fun in our most limitless #Hash"
        send_mail(subject,message,host_email,[sender_mail])
        messages.success(request, "Your account has been succesfully created.")
        return redirect('signin')
    return render(request,'signup.html')


def signout(request):
    # Record logout time
    user = request.user
    if user.is_authenticated:
        screen_time= ScreenTime.objects.filter(user=user).latest('user')
        screen_time.logout_time = timezone.now()
        screen_time.update_time_spent()

        profile=Profile.objects.get(user=request.user)
        profile.status=False
        profile.save()
        
        logout(request)
        messages.success(request, "Logged out Successfully")
    return redirect('frontpage')

def password_change(request):
    user = request.user.id
    profile = Profile.objects.get(user=request.user)
    if request.method=="POST":
        current = request.POST["oldpass1"]
        new_pas = request.POST["pass1"]
        confirm_pas = request.POST["pass2"]
        user = User.objects.get(id=request.user.id)
        un = user.username

        check = user.check_password(current)
        if check==True:
            if  new_pas==confirm_pas:
                user.set_password(new_pas)
                user.save()
                messages.success(request, "Password Changed Successfully")
                user = User.objects.get(username=un)
                login(request,user)
            else:
                messages.success(request, "The Passwords does not match")
        else:
            messages.success(request, "Incorrect Current Password")
        return redirect('password_change')
    return render(request,'change-password.html')



# List Posts in Feed

def feed(request):
    user = request.user
    posts=Post.objects.filter(Q(user__profile__followers=request.user.profile) | Q(user=request.user))
    # posts = Stream.objects.filter(user=user)
    group_ids = [post.id for post in posts]
    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')
    for post in post_items:
        post.user_has_liked = post.likes.filter(id=user.id).exists()

    profile = Profile.objects.all()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # If it's an AJAX request, return post comments in JSON format
        comments_data = []
        for post in post_items:
            comments_data.append({
                'post_id': post.id,
                'comments': [{'text': comment.text} for comment in post.comments.all()]
            })
        return JsonResponse({'comments_data': comments_data})
    # Fetch comments for each post using set()
    for post in post_items:
        post.comments.set(Comment.objects.filter(post=post).order_by('created'))
    comment_form = CommentForm()
    context = {
        'post_items': post_items,
        'profile': profile,
        'comment_form': comment_form,
    }
    return render(request, 'feed.html', context)

#Like with Ajax
def like(request):
    data = json.loads(request.body)
    id = data["id"]
    post = Post.objects.get(id=id)
    checker = 0

    if request.user.is_authenticated:
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            checker = 0
        else:
            post.likes.add(request.user)
            Notification.objects.create(sender=request.user, receiver=post.user , body="liked your post", post=post)
            checker = 1
    likes = post.likes.count()
    info = {
        "check": checker,
        "num_of_likes": likes
    }
    return JsonResponse(info, safe=False)

#Form submission with AJAX
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user  # Associate the comment with the logged-in user
            comment.post = post
            comment.save()
            Notification.objects.create(sender=request.user, receiver=post.user , body="commented : ", post=post, comment=comment )
            return JsonResponse({'success': True, 'message': 'Comment added successfully'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

#Fetching comments with AJAX
def fetch_post_comments(request, post_id):
    try:
        post = get_object_or_404(Post, id=post_id)
        comments = Comment.objects.filter(post=post)
        comment_data = []
        for comment in comments:
            comment_data.append({
                'user': {
                    'username': comment.user.username,
                    'profile_picture': comment.user.profile.image.url if comment.user.profile.image else None,
                },
                'text': comment.text,
            })
        return JsonResponse({'comments': comment_data})
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)



#Search
def search(request):
    q = request.GET.get('search') if request.GET.get('search') != None else ""
    user_results = User.objects.filter( Q(username__istartswith=q) | Q(profile__full_name__istartswith=q) ) 
    tag_results = Tag.objects.filter( Q(title__istartswith=q))
    context = {
        'userresults' : user_results,
        'tagresults' : tag_results
    }
    return render(request, "find.html", context)





def screen_time_view(request):
    # Calculate the start and end of the current week (assuming Monday is the start of the week)
    current_date = datetime.now()
    start_of_week = current_date - timedelta(days=current_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)


    screen_times = ScreenTime.objects.filter(login_time__date__range=[start_of_week.date(), end_of_week.date()])

    # Initialize a dictionary to store the screen time data for each day of the week
    screen_time_data = {'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0, 'Sunday': 0}

    # Calculate the screen time data for each day of the week
    for screen_time in screen_times:
        day_name = screen_time.login_time.strftime('%A')  # Get the name of the day of the week
        screen_time_data[day_name] += screen_time.time_spent_seconds

    # Convert screen time data to hours and handle cases where data is missing
    bar_data = {day: (time_spent / 3600) for day, time_spent in screen_time_data.items()}

    # Pass the combined data to the template
    context = {
        'bar_data': bar_data,
    }

    return render(request, 'weekly_screentime_graph.html', context)

def liketweet(request):
    data = json.loads(request.body)
    id = data["id"]
    tweet = Tweet.objects.get(id=id)
    checker = 0

    if request.user.is_authenticated:
        if tweet.likes.filter(id=request.user.id).exists():
            tweet.likes.remove(request.user)
            checker = 0
        else:
            tweet.likes.add(request.user)
            Notification.objects.create(sender=request.user, receiver=tweet.user , body="liked your tweet")
            checker = 1
    likes = tweet.likes.count()
    info = {
        "check": checker,
        "num_of_likes": likes
    }
    return JsonResponse(info, safe=False)

#Create New Post
@login_required
def NewPost(request):
    user = request.user.id
    tags_objs = []

    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = request.POST.get('caption')
            tag_form = request.POST.get('tag')
            tags_list = list(tag_form.split(' '))

            for tag in tags_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_objs.append(t)
            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user_id=user)
            p.tag.set(tags_objs)
            p.save()
        return redirect('feed')
    else:
        form = NewPostForm()
    context = {
        'form': form
    }
    return render(request, 'newpost.html', context)


def TweetDetail(request,id):
    if request.method=="POST":
        current_tweet = get_object_or_404(Tweet, id=id)
        body=request.POST['reply']
        print(body)
        if body:
            Reply.objects.create(user=request.user,tweet=current_tweet,reply=body)
    tweet = get_object_or_404(Tweet, id=id)
    replies = Reply.objects.filter(tweet=tweet).order_by('-created')
    profile = get_object_or_404(Profile, user=tweet.user)
    user = request.user
    tweet.user_has_liked = tweet.likes.filter(id=user.id).exists()
    context = {
        'tweet' : tweet,
        'profile' : profile,
        'replies' : replies
    }
    return render(request, 'tweet-details.html', context)


#Detailed Post page
def PostDetail(request,username,slug):
    post = get_object_or_404(Post, slug=slug)
    profile = get_object_or_404(Profile, user=post.user)
    user = request.user
    post.user_has_liked = post.likes.filter(id=user.id).exists()
    context = {
        'post' : post,
        'profile' : profile,
    }
    return render(request, 'post-details.html', context)


#Tag filtering posts
def tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tag=tag).order_by('-posted')
    context = {
        'tag' : tag,
        'posts' : posts
    }
    return render(request, 'tags.html', context)


def notifications(request):
    user = request.user
    noti = Notification.objects.filter(receiver=user).order_by('-created')
    profile=Profile.objects.all()
    context={
        'noti' : noti,
        'profile':profile,
    }
    return render(request, 'notifications.html', context)

#Savepost
def saved(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)
    if profile.saved.filter(id=post_id).exists():
        profile.saved.remove(post)
    else:
        profile.saved.add(post)
    return HttpResponseRedirect(reverse('feed'))


# def test(request):
#     user = request.user
#     posts = Post.objects.all().order_by('-posted')
#     return render(request,'test.html', {'post_items':posts})


def profile(request,username):
     # Calculate the start and end of the current week (assuming Monday is the start of the week)
    current_date = datetime.now()
    start_of_week = current_date - timedelta(days=current_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    screen_times = ScreenTime.objects.filter(login_time__date__range=[start_of_week.date(), end_of_week.date()])

    # Initialize a dictionary to store the screen time data for each day of the week
    screen_time_data = {'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0, 'Sunday': 0}

    # Calculate the screen time data for each day of the week
    for screen_time in screen_times:
        day_name = screen_time.login_time.strftime('%A')  # Get the name of the day of the week
        screen_time_data[day_name] += screen_time.time_spent_seconds

    # Convert screen time data to hours and handle cases where data is missing
    bar_data = {day: (time_spent / 3600) for day, time_spent in screen_time_data.items()}

    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name
    if url_name == 'profilee':
        posts = Post.objects.filter(user=user).order_by('-posted')
        tweets=None
    elif url_name == 'savedd':
        posts = profile.saved.all()
        tweets=None
        bar_data=None
    elif url_name == 'screentime':
        posts=None
        tweets=None
    elif url_name == 'thoughts':
        tweets=Tweet.objects.filter(user=user).order_by('-updated')
        for tweet in tweets:
            tweet.user_has_liked = tweet.likes.filter(id=user.id).exists()
        posts=None
    
    context = {
        'profile' : profile,
        'posts' : posts,
        'tweets':tweets,
        'url_name' : url_name,
        'bar_data': bar_data,
    }
    return render(request, 'profile.html', context)

#Our Profileollow
# @login_required
# def my_profile(request):
#     username = request.user.username
#     return redirect('profilee', username=username)

# def navbar(request):
#     user = request.user
#     profile = Profile.objects.get(user=user)
#     context = {
#         'profile' : profile
#     }
#     return render(request, 'header.html', context)

#Follow function
# def follow(request, username, option):
#     user = request.user
#     following = get_object_or_404(User, username=username)
#     try:
#         f, created = Follow.objects.get_or_create(follower=user, following=following)
#         if int(option) == 0 :
#             f.delete()
#             Stream.objects.filter(following=following, user=user).all().delete()
#         else:
#             posts = Post.objects.filter(user=following)[:10]
#             Notification.objects.create(sender=request.user, receiver=following , body="followed you")

#             with transaction.atomic():
#                 for post in posts:
#                     stream = Stream(post=post, user=user, date=post.posted, following=following)
#                     stream.save()
#         return HttpResponseRedirect(reverse('profilee', args=[username]))
#     except User.DoesNotExist:
#         return HttpResponseRedirect(reverse('profilee', args=[username]))

#Create profile

def createProfile(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        form = CreateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profilee', username=request.user.username)
    
    form = CreateProfileForm()

    context = {
        'form': form,
    }
    return render(request, 'create-profile.html', context)

#Edit profile
def editProfile(request):
    user = request.user.id
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        em = request.POST['email']
        un = request.POST['username']
        usr = User.objects.get(id=user)
        usr.email=em
        usr.username=un
        usr.save()
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profilee', username=request.user.username)
    else:
        form = EditProfileForm(instance=profile)

    context = {
        'form': form,
        'profile':profile,
    }
    return render(request, 'edit-profile.html', context)



def createtweet(request):
    if request.method=="POST":
        tweet = request.POST['tweet']
        Tweet.objects.create(user=request.user,tweet=tweet)
        return redirect('tweetfeed')
    return render(request, 'newtweet.html')


def followuser(request,id,status):
    req_user=Profile.objects.get(user=request.user)
    follow_user=Profile.objects.get(user=id)
    if status == 1:
        follow_user.followers.add(req_user)
        follow_user.save()
        Notification.objects.create(sender=request.user, receiver=follow_user.user , body="followed you")
    if status == 0:
        follow_user.followers.remove(req_user)
        follow_user.save()
    return redirect('profilee', username=follow_user.user.username)
