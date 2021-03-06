from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings
from .models import Tweet
from .forms import TweetForm
import random


# Create your views here.
ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args,**kwargs):
    return render(request, 'pages/home.html', {})

def tweet_detail_view(request, tweet_id, *args, **kwargs):

    """
    REST API view to be consumed by JS
    """


    data={
        'tweet_id' : tweet_id,
        'likes' : random.randint(0,100)
        # 'image_path' : tweet.
    }
    status = 200
    try:
        tweet = Tweet.objects.get(id=tweet_id)
        data['content']  = tweet.content
    except:
        data['message'] = 'Not Found'
        status = 404

    return JsonResponse(data, status=status)
    
def tweet_list_view(request, *args, **kwargs):

    """
    REST API view to be consumed by JS
    """
    
    tweets = Tweet.objects.all()
        
    tweets_list = [tweet.serialize() for tweet in tweets]
    data ={
        "response" : tweets_list
    }
    return JsonResponse(data)


def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)

        if is_safe_url(next_url, ALLOWED_HOSTS) :
            return redirect(next_url)
            
        form = TweetForm()
    
    if form.errors and request.is_ajax():
        return JsonResponse(form.errors, status=400)

    return render(request, 'components/form.html', {'form' : form})
