from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required

from network.forms import PostForm, CommentForm
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
        logged_status = request.user.is_authenticated
        if post_id:
            try:
                post = Post.objects.get(id=post_id)
                comments = Comment.objects.filter(posted_in=post)
                attitudes = Attitude.objects.filter(liked_in=post)
                return render(request, self.view_template_name, {'post': post, 'comments': comments,
                                                                 'attitudes': attitudes, 'logged_status': logged_status})            
            except Post.DoesNotExist:
                return render(request, self.view_template_name, {'post': None})
        else:
            form = PostForm()
            return render(request, self.creation_template_name, {'form': form})

    @login_required
    def post(self, request, post_id=None):

        if post_id:
            try:
                post = Post.objects.get(id=post_id)
                form = PostForm(request.POST, instance=post)
            except Post.DoesNotExist:
                return redirect(self.view_template_name)
            social_user = SocialUser.objects.get(id=request.user.id)
            attitudes = Attitude.objects.filter(liked_in=post)

            if 'like' in request.POST:
                attitude = True
            elif 'dislike' in request.POST:
                attitude = False
            else:
                attitude = None
            
            if attitude is not None:
                Attitude.objects.create(author=social_user, liked_in=post, like=attitude)

            return render(request, self.view_template_name, {'post': post, 'attitudes': attitudes, 'logged_status': True})
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


def view_posts(request, social_user_id=None):
    if social_user_id is None:
        social_user = None
        posts = Post.objects.all()
    else:
        try:
            social_user = SocialUser.objects.get(id=social_user_id)
            posts = Post.objects.filter(author=social_user)
        except SocialUser.DoesNotExist:
            social_user = None
            posts = Post.objects.all()
    return render(request, 'view_posts.html', {'posts': posts, 'social_user': social_user})


@login_required
def comments_view(request, post_id=None, social_user_id=None):
    post = None
    social_user = None
    no_comment = True
    if post_id is not None:
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return render(request, 'comments.html', {'error': 'Post not found'})
        comments = Comment.objects.filter(posted_in=post)
        no_comment = False
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.posted_in = post
            comment_user_id = request.user.id
            comment_user = SocialUser.objects.get(id=comment_user_id)
            comment.author = comment_user
            comment.save()
        return render(request, 'comments.html', {'comments': comments, 'post': post,
                                                 'social_user': social_user, 'error': None,
                                                 'no_comment': no_comment, 'form': comment_form})       

    elif social_user_id is not None:
        try:
            social_user = SocialUser.objects.get(id=social_user_id)
            comments = Comment.objects.filter(author=social_user)
            return render(request, 'comments.html', {'comments': comments, 'social_user': social_user, 'no_comment': no_comment})
        except SocialUser.DoesNotExist:
            return render(request, 'comments.html', {'error': 'User not found'})
    else:
        comments = Comment.objects.all()

        return render(request, 'comments.html', {'comments': comments, 'no_comment': no_comment})   
