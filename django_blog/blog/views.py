from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, CreateView
from django.views.generic import ListView, DeleteView, UpdateView, DetailView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileForm, PostForm, CommentForm
from .models import Post, CustomUser, Comment, Tag
# Create your views here.

class RegisterView(CreateView):
    model = CustomUser
    template_name = 'blog/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        print("Form is valid")
        response = super().form_valid(form)
        print("User created")
        return response

    def form_invalid(self, form):
        print("Form is invalid")
        return super().form_invalid(form)


class PostView(FormView):
    posts = Post.objects.all()
    template_name = 'blog/posts.html'

class HomeView(FormView):
    template_name = 'blog/home.html'


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, 'blog/profile.html', {"form": form, "user": request.user})


class  PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Optionally add or modify additional context data here
        return context
    
# views.py
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['form'] = CommentForm()
        context['tags'] = self.object.tags.all()
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
        return self.get(request, *args, **kwargs)
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        form.save_m2m()
        return response
    
class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def handle_no_permission(self):
        return redirect('post_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        return response
    

class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('post_list')
    context_object_name = 'post'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Optionally add or modify additional context data here
        return context

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
    
    def handle_no_permission(self):
        return redirect('post_list')

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # Create a form instance without saving
            post.author = request.user      # Set the author to the current user
            post.save()                    # Save the blog post
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})

@login_required
def update_post(request, pk):
    blog_post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=blog_post)
        if form.is_valid():
            form.save()  # Save the updated blog post
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=blog_post)
    return render(request, 'post_form.html', {'form': form})

class CommentEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/edit_comment.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        comment = self.get_object()
        return reverse_lazy('post_detail', kwargs={'pk': comment.post.pk})
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/delete_comment.html'



    def get_success_url(self):
        comment = self.get_object()
        return reverse_lazy('post_detail', kwargs={'pk': comment.post.pk})
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

def search_view(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    else:
        posts = Post.objects.none()
    
    return render(request, 'blog/search_results.html', {'posts': posts, 'query': query})

def tagged_posts_view(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag)
    return render(request, 'blog/tagged_posts.html', {'posts': posts, 'tag': tag})