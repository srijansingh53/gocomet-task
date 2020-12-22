from django.http import JsonResponse
from django.shortcuts import render
from django.template import loader
from django.contrib import messages

# from .forms import UserForm
# from .models import Tags
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .scrap2 import get_blogs

# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request, 'medium/base.html')

def search(request):

    if request.method == 'GET':
        tag = request.GET.get("tag", None)
        print(tag)
        data = get_blogs(str(tag),page=1)

        if data is None:
            JsonResponse({'tags': "<h2>Search a Valid Tag</h2>",}, status=200)

        blogs_per_page = 10
        paginator = Paginator(data['blogs'], blogs_per_page)

        related_tags = data['tags']
        tags_html = loader.render_to_string('medium/tags.html', {'tags': related_tags})

        # print(paginator.page(1).has_next())
        blogs = paginator.page(1)
        if len(blogs)==0:
            blogs_html = loader.render_to_string('medium/blogs.html', {'error': 'No blogs found. Please enter valid tag'})
        else:
            blogs_html = loader.render_to_string('medium/blogs.html', {'blogs': blogs})
        
        
        return JsonResponse({
            'tag': tag,
            'tags': tags_html,
            'blogs': blogs_html,
            'has_next': blogs.has_next(),
            'has_prev': blogs.has_previous()}, status=200)

def other_page(request):
    
    if request.method=='POST':
        page = request.POST.get('page')
        page = int(page)
        print(page)
        tag = request.POST.get('tag')

        data = get_blogs(str(tag), page)

        blogs_per_page = 10
        paginator = Paginator(data['blogs'], blogs_per_page)

        try:
            blogs = paginator.page(page)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)

        blogs_html = loader.render_to_string('medium/blogs.html', {'blogs': blogs})
        print(blogs.has_previous())
        return JsonResponse({
            'blogs': blogs_html,
            'tag': tag,
            'has_next': blogs.has_next(),
            'has_prev': blogs.has_previous()}, status = 200)