from django.shortcuts import render


# Create your views here.
def landing(request):
    return render(request, 'single_pages/landing.html',{
        recent_posts = Post.objects_order_by('-pk')[:3]

    })


def about_me(request):
    return render(request, 'single_pages/about_me.html')
