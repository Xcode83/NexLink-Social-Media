from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Profile, FriendRequest, Friendship, Message, Comment
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, PostForm, CommentForm
from django.contrib.auth.models import User
from django.db import models

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'social/register.html', {'form': form})

@login_required
def home(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('home')
    else:
        form = PostForm()
    
    posts = Post.objects.all()
    comment_form = CommentForm()
    return render(request, 'social/home.html', {'posts': posts, 'form': form, 'comment_form': comment_form})

@login_required
def profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user_obj)
    comment_form = CommentForm()
    is_following = request.user.profile.following.filter(id=user_obj.profile.id).exists()
    is_followed_by = user_obj.profile.following.filter(id=request.user.profile.id).exists()
    
    return render(request, 'social/profile.html', {
        'user_obj': user_obj, 
        'posts': posts,
        'comment_form': comment_form,
        'is_following': is_following,
        'is_followed_by': is_followed_by
    })

@login_required
def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile', username=request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'social/profile_update.html', context)

@login_required
def explore(request):
    profiles = Profile.objects.exclude(user=request.user)
    # Add relationship context to each profile
    for profile in profiles:
        profile.is_following = request.user.profile.following.filter(id=profile.id).exists()
        profile.is_followed_by = profile.following.filter(id=request.user.profile.id).exists()
    return render(request, 'social/explore.html', {'profiles': profiles})

@login_required
def search_users(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = User.objects.filter(username__icontains=query).exclude(id=request.user.id)
    return render(request, 'social/search_results.html', {'results': results, 'query': query})

@login_required
def send_friend_request(request, username):
    to_user = get_object_or_404(User, username=username)
    if not FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        messages.success(request, f'Friend request sent to {username}!')
    return redirect('profile', username=username)

@login_required
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)
    target_profile = target_user.profile
    my_profile = request.user.profile

    if my_profile == target_profile:
        messages.error(request, "You cannot follow yourself!")
    elif my_profile.following.filter(id=target_profile.id).exists():
        my_profile.following.remove(target_profile)
        messages.success(request, f"You stopped following {username}.")
    else:
        my_profile.following.add(target_profile)
        messages.success(request, f"You are now following {username}.")
    
    return redirect(request.META.get('HTTP_REFERER', 'profile'), username=username)

@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    friendship = Friendship.objects.create()
    friendship.users.add(request.user, friend_request.from_user)
    friend_request.delete()
    messages.success(request, 'Friend request accepted!')
    return redirect('profile', username=friend_request.from_user.username)

@login_required
def inbox(request):
    # Get all users the current user has exchanged messages with
    sent_to = Message.objects.filter(sender=request.user).values_list('receiver', flat=True)
    received_from = Message.objects.filter(receiver=request.user).values_list('sender', flat=True)
    user_ids = set(list(sent_to) + list(received_from))
    conversations = User.objects.filter(id__in=user_ids)
    
    # Also get pending friend requests
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    
    return render(request, 'social/inbox.html', {
        'conversations': conversations,
        'friend_requests': friend_requests
    })

@login_required
def chat(request, username):
    other_user = get_object_or_404(User, username=username)
    
    # Mutual Follow Check
    is_following = request.user.profile.following.filter(id=other_user.profile.id).exists()
    is_followed_by = other_user.profile.following.filter(id=request.user.profile.id).exists()
    
    if not (is_following and is_followed_by):
        messages.error(request, "Communication is restricted to mutual followers. Follow each other to start talking!")
        return redirect('profile', username=username)

    if request.method == 'POST':
        body = request.POST.get('body')
        if body:
            Message.objects.create(sender=request.user, receiver=other_user, body=body)
            return redirect('chat', username=username)
            
    messages_list = Message.objects.filter(
        (models.Q(sender=request.user, receiver=other_user)) |
        (models.Q(sender=other_user, receiver=request.user))
    ).order_by('timestamp')
    
    return render(request, 'social/chat.html', {
        'other_user': other_user,
        'chat_messages': messages_list
    })

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:
        post.delete()
        messages.success(request, 'Post deleted successfully!')
    else:
        messages.error(request, 'You cannot delete someone else\'s post!')
    return redirect('home')

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def post_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been posted!')
    return redirect(request.META.get('HTTP_REFERER', 'home'))
