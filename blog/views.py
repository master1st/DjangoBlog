from django.shortcuts import render
from .models import Post
# Create your views here.
def index(request):

    posts = Post.objects.all().order_by('-pk')
    return render(request,'blog/index.html',
                  {
                      'posts' : posts,
                  }
                  )

# request의 종류에는 여러가지가 있다. 브라우저에서 어떤 요청을 서버에게 줄 수도 있고해서
# 항상 request를 전달해줘야한다.