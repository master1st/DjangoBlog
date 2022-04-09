from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag



# def index(request):
#
#     posts = Post.objects.all().order_by('-pk')
#
#     return render(request, 'blog/index.html',
#     {
#         'posts': posts,
#     }
#     )
#
# def single_post_page(request,pk):
#     post = Post.objects.get(pk=pk)
#
#     return render(
#         request,
#         'blog/single_post_page.html',
#         {
#             'post': post,
#         }
#     )
#     return None

class PostList(ListView):
    model = Post
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()

        return context


class PostDetail(DetailView):
    model = Post


    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()

        return context


def show_category_posts(request, slug):
    if slug=='no-category' :
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else :
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category = category)
        # 같은 문장 하나더 써져있었음. 참고
    context = {
        'categories' : Category.objects.all(),
        'no_category_post_count' : Post.objects.filter(category=None).count(),
        'category' : category,
        'post_list' : post_list
    }
    return render(request, 'blog/post_list.html', context)


def show_tag_posts(request,slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()


    context = {
        'categories' : Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count(),
        'tag': tag,
        'post_list': post_list
    }
    return render(request, 'blog/post_list.html',context)