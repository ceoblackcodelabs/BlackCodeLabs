from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, View, TemplateView

from .models import Post, Category, Comment
from .forms import CommentForm, ContactForm


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):
        qs = Post.objects.filter(status="published").select_related("category", "author")
        cat = self.request.GET.get("category")
        q = self.request.GET.get("q")
        if cat and cat != "all":
            qs = qs.filter(category__slug=cat)
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(excerpt__icontains=q) | Q(body__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["featured"] = Post.objects.filter(status="published", featured=True).first()
        ctx["active_category"] = self.request.GET.get("category", "all")
        ctx["query"] = self.request.GET.get("q", "")
        return ctx


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        return Post.objects.filter(status="published").select_related("category", "author")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comment_form"] = CommentForm()
        ctx["comments"] = self.object.comments.filter(parent__isnull=True).select_related("author").prefetch_related("replies__author")
        ctx["related"] = Post.objects.filter(status="published").exclude(pk=self.object.pk)[:3]
        ctx["liked"] = self.request.user.is_authenticated and self.object.likes.filter(pk=self.request.user.pk).exists()
        context = {
        # Sidebar data
        'author_post_count': Post.objects.count(),
        'author_comment_count': Comment.objects.count(),
        'popular_posts': Post.objects.filter(status='published')[:5],
        'all_categories': Category.objects.annotate(post_count=Count('posts')),
        }
        ctx.update(context)
        return ctx


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug, status="published")
        form = CommentForm(request.POST)
        parent_id = request.POST.get("parent")
        if form.is_valid():
            c = form.save(commit=False)
            c.post = post
            c.author = request.user
            if parent_id:
                try:
                    c.parent = post.comments.get(pk=parent_id)
                except Comment.DoesNotExist:
                    pass
            c.save()
            messages.success(request, "Your comment was posted.")
        else:
            messages.error(request, "Please write a comment before posting.")
        return redirect(post.get_absolute_url() + "#comments")


class PostLikeView(LoginRequiredMixin, View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug, status="published")
        if post.likes.filter(pk=request.user.pk).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        return JsonResponse({"liked": liked, "count": post.likes.count()})


class CommentLikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        c = get_object_or_404(Comment, pk=pk)
        if c.likes.filter(pk=request.user.pk).exists():
            c.likes.remove(request.user)
            liked = False
        else:
            c.likes.add(request.user)
            liked = True
        return JsonResponse({"liked": liked, "count": c.likes.count()})


class ContactView(CreateView):
    form_class = ContactForm
    template_name = "blog/contact.html"
    success_url = reverse_lazy("blog:contact")

    def form_valid(self, form):
        messages.success(self.request, "Message sent — we'll get back to you soon.")
        return super().form_valid(form)


class AboutView(TemplateView):
    template_name = "blog/about.html"
