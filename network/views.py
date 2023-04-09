import json
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import User,Post,Relationship,Profile
from .serializers import PostSerializer, ProfileSerializer

#from .models import User


def index(request):
    posts = Post.objects.all()
    content =  pagination(request, posts)
    return render(request, "network/index.html", {
        "posts": content,
        
    })


def login_view(request):
     
    if request.method == "POST":
        
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

#@csrf_exempt
@login_required
def newPost(request):
    if request.method != "POST":
        return render(request, "network/index.html")
    
    if request.user.is_authenticated:
        #load the json content
        data = json.loads(request.body)
        #get the body of post
        body = data.get("body", "")
    
        #save into database
        if len(body) > 0:
          post = Post(author = request.user, body = body)
          post.save()

        #serialize
        serialize = PostSerializer(post)

        #send back the post in json fomart
        #index(request)
        return JsonResponse({"message": "successfully posted."}, status=201)
    return render(request, "network/login.html")

# I implemented a method or fumction for to help paginate the pages to avoid repitition.
def pagination(request, posts):

    page_number = int(request.GET.get("page") or 1)
    paginator = Paginator(posts, 10)
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    return page_obj

@login_required(login_url='/login')
def profilePage(request, userName):
    #member = User.objects.filter(username = userName)
    try:
        member = User.objects.get(username=userName)
    except User.DoesNotExist:
        raise Http404("No MyModel matches the given query.")
    #member = User.objects.get(username=userName)
    profile = Profile.objects.filter(user = member)
    

    print(member.username)
    user = request.user
    connect = ""
    
    if user.is_authenticated:
        relation = Relationship.objects.filter(follows = member, follow_by = user)
        if relation:
            connect = "Unfollow"
        elif user != member:
            connect = "Follow"
    posts = member.posts.all()
    content =  pagination(request, posts)

    return render(request, "network/profile.html", {
        "member": member,
        "posts": content,
        "userName": member.username,
        "joinedDate": member.joined_date,
        "followers":member.follows.count(),
        "following":member.follow_by.count(), 
        "related": connect,
        'profile': profile
    })

@login_required
def connection(request, userName):
        member = User.objects.get(username = userName)
        connected = Relationship.objects.filter(follows = member, follow_by = request.user)
        
        related = ""
        if connected:
            connected.delete()
            related = "Follow"
        else:
            connected = Relationship(follows = member, follow_by = request.user)
            connected.save()
            related = "Unfollow"

        print("connected. Done..")
        
        profile = {
           'erro': "You cannot follow yourself",
           "related": related,
           'followers': member.follow_by.count(),
           'following': member.follows.count(),
        }
        
        return JsonResponse(profile, status=200)

@login_required
def following(request):
    user = User.objects.get(username = request.user)
    print(f"user.joined_date: {user.joined_date} ")
    connected = user.follow_by.all()
    postsList = []
    for person in connected:
        postsList += person.follows.posts.all()
    posts = sorted(postsList, key=lambda post: post.timestamp, reverse=True)
    content =  pagination(request, posts)
    return render(request, "network/following.html", {
        "posts": content
    })

@login_required
def editPost(request, postID):
    post = Post.objects.get(author = request.user, pk=postID)
    #if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    if request.method != "PUT":
        return render(request, "network/index.html")
    
    if request.user.is_authenticated:
        #load the json content
        data = json.loads(request.body)
        #get the body of post
        body = data.get("body", "")
    
        #save into database
        if len(body) > 0:
          post.body = body
          post.save()

        #serialize
        serialize = PostSerializer(post)

        #send back the post in json fomart
        #index(request)
        return JsonResponse({"message": "Post sucessfilly updated.",
        "post" : serialize.data}, status=201)
    return render(request, "network/login.html")

@login_required
def likePost(request, postID):
    #user = User.objects.get(username = request.user)
    user = request.user
    if user.is_authenticated:
        post = Post.objects.get(pk=postID)

        likes = post.likes.all()

        if user in likes:
           post.likes.remove(user)
        else:
          post.likes.add(user)
    
        serialize = PostSerializer(post)
        response ={
           'post': serialize.data
  
        }
        return JsonResponse(response, status = 203)
    return render(request, "network/index.html")

#@csrf_exempt
def editProfile(request, userName):
    if request.user.is_authenticated:
        if request.method == "POST" :
            #fields = ['id', 'user', 'name', 'about', 'country', 'photo']
            
            name = request.POST.get("name")
            aboutME = request.POST.get("about")
            country = request.POST.get("country")
            photo =  request.FILES.get("image")
            
            profile = Profile.objects.filter(user= request.user)

            if profile:
               profile.delete()
                
                
            profile = Profile(user = request.user, name = name, about = aboutME, country = country, photo = photo)
            profile.save()
            print(profile)
            serialize = ProfileSerializer(profile)
            response ={
                'profile': serialize.data
            }   
            return JsonResponse(response, status = 201)
        HttpResponseRedirect(reverse("profilePage", kwargs={"userName": userName}))
    return render(request, "network/index.html")




   
   