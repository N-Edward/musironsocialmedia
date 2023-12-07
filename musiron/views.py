from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, LoginForm, UserProfileUpdateForm, PostUploadFoam, CommentForm, UserProfileCreateForm
from django.contrib.auth.decorators import login_required
from . models import Profile, Post, PostComment
from django.contrib.auth.models import User
from django.urls import reverse_lazy


# Create your views here.
#home page
def index(request):
    if request.user.is_authenticated:
        posts = Post.objects.all().order_by('-upload_date')
        current_user = request.user
        user = User.objects.get(username = current_user.username, id = current_user.id)
        prof= Profile.objects.get(user = user)
        profiles = Profile.objects.all()
        users = User.objects.all()
        context = {
            'posts':posts,
            'prof':prof,
            'profiles':profiles,
            'users': users
        }
        return render(request, 'index.html', context)
    else:
        posts = Post.objects.all().order_by('-upload_date')
        return render(request, 'index.html', {'posts':posts})
        


#registration page
def user_signup(request):
    if request.method == 'POST':
        form  = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return redirect('signup')
    else:
        form = UserRegistrationForm()
        return render(request, 'signup.html', {'form':form})
        
        

#login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username, password=password)
            if user:
                login(request,user)
                current_user = User.objects.get(username=request.user.username, id = request.user.id)
                profile = Profile.objects.filter(user = current_user)
                if not profile:
                    return redirect('add_profile')
                return redirect('home')
            else:
                return redirect('login')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form':form})

#logout from system
def user_logout(request):
    logout(request)
    return redirect('login')

# updating user profile
@login_required(login_url='login')
def update_user_profile(request, id):
    if request.method == 'POST':
        prof = Profile.objects.get(id=id)
        user_update_form = UserProfileUpdateForm(request.POST, request.FILES)
        if user_update_form.is_valid():
            location = user_update_form.cleaned_data['location']
            nickname = user_update_form.cleaned_data['nickname']
            prof.location = location
            prof.nickname = nickname
            prof.save()
            return redirect('view-user-profile')
        else:
            form = UserProfileUpdateForm()
            return render(request, 'user_profile_update.html', {'user_update_form':form})
    else:
        form = UserProfileUpdateForm()
        return render(request, 'user_profile_update.html',{'user_update_form':form})
    
#add profile
@login_required(login_url='login')
def create_profile(request):
    if request.method == 'POST':
        current_user = request.user
        user = User.objects.get(username = current_user.username, id = current_user.id)
        form  = UserProfileCreateForm(request.POST, request.FILES)
        if form.is_valid():
            nickname = form.cleaned_data['nickname']
            location = form.cleaned_data['location']
            profile_image = form.cleaned_data['profile_image']
            profile = Profile(nickname=nickname,location=location,profile_image=profile_image,user=user)
            profile.save()
            return redirect('home')
        else:
            form = UserProfileCreateForm()
            return render(request, 'add_profile.html',{'form':form})
    else:
        form = UserProfileCreateForm()
        return render(request,'add_profile.html',{'form':form})
    

#view user profile
@login_required(login_url='login')
def view_user_profile(request):
    user = User.objects.get(username=request.user.username, id = request.user.id)
    profile = Profile.objects.get(user = user)
    posts = Post.objects.filter(author = user).order_by('-upload_date')
    if posts:
        return render(request, 'user_profile.html', {'profile':profile,'posts':posts})
    return render(request, 'user_profile.html', {'profile':profile})
                
                
#fileupload
@login_required(login_url='login')
def user_file_upload(request):
    if request.method =='POST':
        current_user = request.user
        user = User.objects.get(username = current_user.username, id = current_user.id)
        form = PostUploadFoam(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            post_image = form.cleaned_data['post_image']
            post = Post(author=user,title=title,description=description,post_image=post_image)
            post.save()
            return redirect('home')
        else:
            form = PostUploadFoam()
            return render(request, 'user_fileupload.html',{'form':form})
    else:
        form = PostUploadFoam()
        current_user = request.user
        user = User.objects.get(username = current_user.username, id = current_user.id)
        return render(request, 'user_fileupload.html', {'form':form, 'user':user})
    
#post
def view_posts(request):
    posts = Post.objects.all().order_by('-upload_date')
    return render (request, 'view_posts.html', {'posts':posts})

#usercomment
@login_required(login_url='login')
def user_comment(request, id):
    post = Post.objects.get(id=id)
    current_user = request.user
    user = User.objects.get(username=current_user.username, id=current_user.id)
    form = CommentForm(request.POST, request.FILES)
    if form.is_valid():
        rate = form.cleaned_data['rate']
        comment = form.cleaned_data['comment']
        postcomment = PostComment(rate=rate,comment=comment,post=post,author=user)
        postcomment.save()
        return redirect('home')
    else:
        form = CommentForm()
        return render (request, 'comment.html', {'form':form,'post':post})
    
    
#view more about post
def more_about_post(request, id):
    more_post = Post.objects.get(id = id)
    comments = PostComment.objects.filter(post = more_post).order_by('-comment_date')
    posters = User.objects.all()
    profiles = Profile.objects.all()
    if comments:
        return render(request, 'more_about_post.html', {'more_post':more_post, 'comments':comments, 'posters':posters, 'profiles':profiles})
    return render(request, 'more_about_post.html', {'more_post':more_post})
