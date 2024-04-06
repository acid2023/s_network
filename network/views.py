from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from network.forms import SocialUserCreationForm, SocialUserForm, PostForm, CommentForm
from network.models import SocialUser, Post, Comment, Attitude


class PostView(View):
    model = Post
    form_class = PostForm
    creation_template_name = 'make_post.html'
    login_url = 'login'
    view_template_name = 'post_view.html'
    success_url = 'home'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get(self, request, post_id=None):
        if post_id:
            try:
                post = Post.objects.get(id=post_id)
                comments = Comment.objects.filter(posted_in=post)
                attitudes = Attitude.objects.filter(liked_in=post)
                return render(request, self.view_template_name, {'post': post, 'comments': comments, 'attitudes': attitudes})            
            except Post.DoesNotExist:
                return render(request, self.view_template_name, {'post': None})
        else:
            form = PostForm()
            return render(request, self.creation_template_name, {'form': form})

    def post(self, request, post_id=None):
        if not request.user.is_authenticated:
            return redirect('login')

        if post_id:
            try:
                post = Post.objects.get(id=post_id)
                form = PostForm(request.POST, instance=post)
            except Post.DoesNotExist:
                return redirect(self.view_template_name)
            comments = Comment.objects.filter(posted_in=post)
            social_user = SocialUser.objects.get(id=request.user.id)
            attitudes = Attitude.objects.filter(liked_in=post)
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.posted_in = post
                comment.author = social_user
                comment.save()
                #return redirect('post_view', post_id=post.id)
            if 'like' in request.POST:
                attitude = True
            elif 'dislike' in request.POST:
                attitude = False
            else:
                attitude = None
            
            if attitude is not None:
                Attitude.objects.create(author=social_user, liked_in=post, like=attitude)

            return render(request, self.view_template_name, {'post': post, 'comments': comments, 'form': comment_form, 'attitudes': attitudes})
        else:
            form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            social_user = SocialUser.objects.get(id=request.user.id)
            post.author = social_user
            post.save()
            return redirect('post_view', post_id=post.id)

        return render(request, self.creation_template_name, {'form': form})


def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Replace 'home' with the name of your home page
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = SocialUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful.')
            return redirect('login')
    else:
        form = SocialUserCreationForm()
    return render(request, 'register.html', {'form': form})


def users_view(request):
    social_users = SocialUser.objects.all()
    return render(request, 'users_view.html', {'social_users': social_users})


def profile_view(request, user_id):
    try:
        social_user = SocialUser.objects.get(id=user_id)
        return render(request, 'profile_view.html', {'social_user': social_user})
    except SocialUser.DoesNotExist:
        return render(request, 'profile_view.html', {'error': 'User not found'})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = SocialUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SocialUserForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

def login_is_required(request):
    return render(request, 'login_required.html')