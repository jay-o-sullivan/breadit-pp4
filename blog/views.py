from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Post, Comment, Profile, Category
from .forms import CommentForm, PostForm, ProfileForm

class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 6

class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug, status=1)
        comments = post.comments.filter(status=1).order_by("-created_on")
        liked = post.likes.filter(id=request.user.id).exists()
        upvoted = post.upvotes.filter(id=request.user.id).exists()
        downvoted = post.downvotes.filter(id=request.user.id).exists()
        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "upvoted": upvoted,
                "downvoted": downvoted,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug, status=1)
        comments = post.comments.filter(status=1).order_by("-created_on")
        liked = post.likes.filter(id=request.user.id).exists()
        upvoted = post.upvotes.filter(id=request.user.id).exists()
        downvoted = post.downvotes.filter(id=request.user.id).exists()

        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            if request.user.is_authenticated:
                comment.status = 1
            comment.save()
            messages.success(request, 'Comment added successfully.')
            return redirect('post_detail', slug=post.slug)
        else:
            messages.error(request, 'Please correct the errors below.')

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked,
                "upvoted": upvoted,
                "downvoted": downvoted
            },
        )

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully.')
            return redirect('post_detail', slug=post.slug)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class PostLike(View):
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully.')
            return redirect('post_detail', slug=post.slug)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # Ensure the profile is linked to the current user
            profile.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form, 'profile': profile})
@login_required
def post_upvote(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.upvotes.filter(id=request.user.id).exists():
        post.upvotes.remove(request.user)
    else:
        if post.downvotes.filter(id=request.user.id).exists():
            post.downvotes.remove(request.user)
        post.upvotes.add(request.user)
    return redirect('post_detail', slug=slug)

@login_required
def post_downvote(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.downvotes.filter(id=request.user.id).exists():
        post.downvotes.remove(request.user)
    else:
        if post.upvotes.filter(id=request.user.id).exists():
            post.upvotes.remove(request.user)
        post.downvotes.add(request.user)
    return redirect('post_detail', slug=slug)
