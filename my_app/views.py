import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models

BASE_CRAIGLIST_URL = 'https://colombia.craigslist.org/search/sss?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
    return render(request, template_name='base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    search_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    response = requests.get(search_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})
    final_postings= []

    for post in post_listings:
        post_titles = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'
    
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'https://craiglist.org/images/peace.jpg'
            
        final_postings.append((post_titles, post_url, post_price, post_image_url))


    frontend_stuff = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html', frontend_stuff)
