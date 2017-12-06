from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import PostForm, UserForm
from .models import Post
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_post(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.post_logo = request.FILES['post_logo']
            file_type = post.post_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'post': post,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'music/create_post.html', context)
            post.save()
            return render(request, 'music/detail.html', {'post': post})
        context = {
            "form": form,
        }
        return render(request, 'music/create_post.html', context)


def detail(request, post_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        user = request.user
        post = get_object_or_404(Post, pk=post_id)
        return render(request, 'music/detail.html', {'post': post, 'user': user})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        posts = Post.objects.filter(user=request.user)
        query = request.GET.get("q")
        if query:
            posts = posts.filter(
                Q(post_title__icontains=query) |
                Q(author__icontains=query)
            ).distinct()
            song_results = song_results.filter(
                Q(song_title__icontains=query)
            ).distinct()
            return render(request, 'music/index.html', {
                'posts': posts,
                'songs': song_results,
            })
        else:
            return render(request, 'music/index.html', {'posts': posts})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'music/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                posts = Post.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'posts': posts})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                posts = Post.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'posts': posts})
    context = {
        "form": form,
    }
    return render(request, 'music/register.html', context)
