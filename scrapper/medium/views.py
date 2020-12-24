from django.http import JsonResponse
from django.shortcuts import render
from django.template import loader
from django.contrib import messages
from django.core.serializers import serialize

# from .forms import UserForm
from .models import Tags, Blogs, Responses
from django.core.paginator import Paginator, EmptyPage

from .scrape import get_blogs, get_details

# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request, 'medium/base.html')

def search(request):

    if request.method == 'GET':
        tag = request.GET.get("tag", None)
        print(tag)

        # saving to Tags models
        link = "https://medium.com/tag/" + tag.replace(' ', '-')
        tag_db = Tags(tags=tag.lower(), link=link.lower())
        tag_db.save()
        print('tag_saved')

        #scrapping latest blogs
        data = get_blogs(str(tag),page=1)

        if data is None:
            return JsonResponse({'tags': "<h2>Incorrect Query. Please search a valid Tag</h2>",}, status=200)

        blogs_per_page = 10
        paginator = Paginator(data['blogs'], blogs_per_page)

        related_tags = data['tags']
        tags_html = loader.render_to_string('medium/tags.html', {'tags': related_tags})

        # print(paginator.page(1).has_next())
        blogs = paginator.page(1)

        # saving the blogs to database
        for blog in blogs:
            # print(blog['title'])
            blog_db = Blogs(
                title = blog['title'], 
                link = blog['link'], 
                writer = blog['writer'],
                )

            blog_db.save()
            print("blog saved")


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
        # print(page)
        tag = request.POST.get('tag')

        data = get_blogs(str(tag), page)

        blogs_per_page = 10
        paginator = Paginator(data['blogs'], blogs_per_page)

        try:
            blogs = paginator.page(page)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)
        
        # saving the blogs to database
        for blog in blogs:
            blog_db = Blogs(
                title = blog['title'], 
                link = blog['link'], 
                writer = blog['writer'],
                )
            
            blog_db.save()
            print("blog saved")

        blogs_html = loader.render_to_string('medium/blogs.html', {'blogs': blogs})
        print(blogs.has_previous())
        return JsonResponse({
            'blogs': blogs_html,
            'tag': tag,
            'has_next': blogs.has_next(),
            'has_prev': blogs.has_previous()}, status = 200)


def crawl_details(request):

    if request.method=='GET':
        link = request.GET.get('link')

        data = get_details(link)

        # saving article description to database
        date,time = data['date_time'].split('·')
        print(date, time)


        blog = Blogs.objects.get(link = link)
        blog.date = date
        blog.read_time = time
        blog.num_claps = data['num_claps']
        blog.num_responses = data['num_responses']
        blog.set_tags(data['related_tags'])
        blog.save()

        # saving responses to database
        for comment in data['comments_list']:
            try:
                comment_db = Responses(blog=blog, responder = comment['responder'], comment = comment['comment'])
                comment_db.save()
            except:
                pass #passing because already present

    detail_html = loader.render_to_string('medium/detail.html', data)
    return JsonResponse({"detail": detail_html}, status = 200)

def show_history(request):
    if request.method=='GET':
        searched_tags = Tags.objects.all()

        searched_tags_html = loader.render_to_string('medium/history.html', {'searched_tags': searched_tags})
        return JsonResponse({"history_tags": searched_tags_html}, status = 200)