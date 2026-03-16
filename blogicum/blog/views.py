from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm
from django.core.paginator import Paginator


class UserCreateView(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/registration_form.html'


def index(request):
    post_list = Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')

    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/index.html', {
        'page_obj': page_obj
    })


def post_detail(request, id):
    post = get_object_or_404(
        Post,
        id=id,
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )

    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    posts = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')

    context = {
        'category': category,
        'posts': posts
    }

    return render(request, 'blog/category.html', context)
