# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from article.models import Article
from django.http import Http404
from django.contrib.syndication.views import Feed
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def home(request):
    posts = Article.objects.all()
    paginator = Paginator(posts, 2, orphans=0, allow_empty_first_page=True)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.paginator(paginator.num_pages)
    return render(request, 'home.html', {'posts': posts})

def detail(request, id):
    try:
        post = Article.objects.get(id = str(id))
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'post.html', {'post': post})

def archives(request):
    try:
        posts = Article.objects.all()
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'archives.html', {'post': posts, 'error': False})

def search_tag(request, tag):
    print 'tag: %s' % tag
    try:
        posts = Article.objects.filter(category__iexact = tag)
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'tag.html', {'posts': posts})

def about_me(request):
    return render(request, 'aboutme.html')

def blog_search(request):
    if 's' in request.GET:
        s = request.GET['s']
        if not s:
            return render(request, 'home.html')
        else:
            posts = Article.objects.filter(title__icontains = s)
            if len(posts) == 0:
                return render(request, 'archives.html', {'posts': posts, 'error': True})
            else:
                return render(request, 'archives.html', {'posts': posts, 'error': False})
    return redirect("/")

class RSSFeed(Feed):
    title = "RSS feed - article"
    link = "feed/posts"
    description = "RSS feed - blog posts"

    def items(self):
        return Article.objects.order_by("-date_time")

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.date_time

    def item_description(self, item):
        return item.content
