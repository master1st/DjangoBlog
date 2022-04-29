from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import CommentForm
from .models import Post, Category, Tag


# def index(request):
#
# post 객체의 모든 post들을 다 가져와서 posts에 담음 .order_by('-pk')는 pk를 거꾸로 post를 나열
#     posts = Post.objects.all().order_by('-pk')
#
# Post객체에서 가져온 모든 값들을 posts에 넣어준다음 , 그것을 templete에 전달.
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
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'hook', 'head_image', 'file_upload', 'category']

    template_name = 'blog/post_form_update.html'

    # 이곳에서 get/post 메소드 구분이 가능하며, 작성자인 author와 현재 로그인한 사용자가 같은 사람인지를 체크
    def dispatch(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.is_authenticated and current_user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


# LoginRequiredMixin 은 로그인하지않은 사용자가 post 글 쓰기에 접근하려고하면 차단
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'hook', 'head_image', 'file_upload', 'category']

    # UserPassesTestMixin 은 특정사용자만 접근을 허용하도록 . 최고권한 admin인지 staff인지 확인
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    # 값의 유효성 검사, request 데이터안에 들어있는 로그인사용자 세션을 가져와 현재 유저에 담아주고, 그것을 토대로
    # 조건문에 권한을 걸어두고, super 하던 글쓰기 작업을 계속한다. redirect는 로그인한 사용자가아니거나, 권한이 글쓰기 허락된 권한이 아닐경우, /blog/(메인)로 보내버림.
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff):
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')


class PostList(ListView):
    model = Post
    ordering = '-pk'

    # CBV방식은 FBV방식과 다르게 이미 기정의된 클래스 라이브러리를 상속받아 정의된 기능을 사용하는것
    # postlist역시 포스트들을 가져와서 나열해주는 역할만하고, 즉 post에 대한 정보만 들어있고, 다른 데이터를 같이 매개변수로 전달해주고싶다면,
    # 그렇다면 get_context_data 메서드라이브러리를 사용해서, context 딕셔너리에 담아 데이터전달.
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
        context['comment_form'] = CommentForm
        return context


def show_category_posts(request, slug):
    if slug == 'no-category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)
        # 같은 문장 하나더 써져있었음. 참고
    context = {
        'categories': Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count(),
        'category': category,
        'post_list': post_list
    }
    return render(request, 'blog/post_list.html', context)


def show_tag_posts(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    context = {
        'categories': Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count(),
        'tag': tag,
        'post_list': post_list
    }
    return render(request, 'blog/post_list.html', context)


def addComment(request,pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post,pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied