from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import SignUpForm, BlogPostForm
from .models import Profile, BlogPost, BlogCategory
from django.contrib.auth import logout
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            
            # Authenticate and login
            user = authenticate(username=username, password=form.cleaned_data.get('password1'))
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    try:
        profile = Profile.objects.get(user=request.user)
        context = {
            'user': request.user,
            'profile': profile,
        }
        
        if profile.user_type == 'doctor':
            # Get doctor's blog posts
            blog_posts = BlogPost.objects.filter(author=request.user)
            context['blog_posts'] = blog_posts
            return render(request, 'accounts/doctor_dashboard.html', context)
        else:
            categories = BlogCategory.objects.all()
            blog_posts_by_category = {}
            for category in categories:
                posts = BlogPost.objects.filter(category=category, status='published')[:3] 
                if posts:
                    blog_posts_by_category[category] = posts
            context['blog_posts_by_category'] = blog_posts_by_category
            return render(request, 'accounts/patient_dashboard.html', context)
            
    except Profile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('signup')

@login_required
def create_blog_post(request):
    try:
        profile = Profile.objects.get(user=request.user)
        if profile.user_type != 'doctor':
            messages.error(request, 'Only doctors can create blog posts.')
            return redirect('dashboard')
    except Profile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('signup')
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            messages.success(request, 'Blog post created successfully!')
            return redirect('dashboard')
    else:
        form = BlogPostForm()
    
    return render(request, 'accounts/create_blog_post.html', {'form': form})

@login_required
def edit_blog_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id, author=request.user)
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated successfully!')
            return redirect('dashboard')
    else:
        form = BlogPostForm(instance=post)
    
    return render(request, 'accounts/edit_blog_post.html', {'form': form, 'post': post})

@login_required
def delete_blog_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id, author=request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Blog post deleted successfully!')
        return redirect('dashboard')
    
    return render(request, 'accounts/delete_blog_post.html', {'post': post})

@login_required
def view_blog_posts(request):
    categories = BlogCategory.objects.all()
    selected_category = request.GET.get('category')
    
    if selected_category:
        posts = BlogPost.objects.filter(category__name=selected_category, status='published')
        category_name = selected_category
    else:
        posts = BlogPost.objects.filter(status='published')
        category_name = 'All Categories'
    
    paginator = Paginator(posts, 6)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'posts': page_obj,
        'categories': categories,
        'selected_category': selected_category,
        'category_name': category_name,
    }
    
    return render(request, 'accounts/view_blog_posts.html', context)

@login_required
def blog_post_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id, status='published')
    return render(request, 'accounts/blog_post_detail.html', {'post': post})