from scraper.models import Movie
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.utils import simplejson
from datetime import datetime  
from django.conf import settings
from django.template import RequestContext
from base64 import decodestring
'''SOS danger disabling CSRF to allow upload from json - for testing 1/2 '''
from django.views.decorators.csrf import csrf_exempt     
from django.core import serializers

from io import StringIO
from django.db.models import Model
from django.db.models.query import QuerySet
from django.utils.encoding import smart_unicode
from django.utils.simplejson import dumps

# Create your views here.
import urllib2
from random import randint
import time
from bs4 import BeautifulSoup # if you're using BeautifulSoup4 OR 
#from BeautifulSoup import BeautifulSoup


@csrf_exempt 
def test(request):
    movie = Movie(urlid=0, title=1, descr=2, year=8, genre=3, 
                  director=4, actor=5, rated=6, rating=7, date_created=datetime.now())
    movie.save()
        
    aaa = 222
    print aaa
    return HttpResponse(aaa);


def netflix(request):
    # parse soup: http://www.crummy.com/software/BeautifulSoup/bs3/download/2.x/documentation.html
    #number = 60001672 #60001621-60014228 #70140300 -> 70178217 , 70180300, 70197040
    for number in range(70200100,70209100): 
        print "-----"
        try:
            url = 'http://movies.netflix.com/WiMovie/' + str(number)
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page)  
            print url #print soup
            #except urllib2.URLError:
            #    print 'Failed to fetch ' + URL
            #except HTMLParser.HTMLParseError:
            #    print 'Failed to parse ' + URL
        
            #eg. <title>movie name</title>
            #titleTag = soup.title
            #title = titleTag.string
            #print title
        
            #fix
            title = soup.findAll('h1',{'class':'title'})[0]
            print title.string  
                    
            #eg. <p class="synopsis" itemprop="description">Bla bla bla
            desc = ''
            decription = soup.findAll('p',{'class':'synopsis'})[0]
            if decription.string is None:
                desc = ''
            else:
                desc = decription.string
    
            #eg. <span class="year">1965
            year = soup.findAll('span',{'class':'year'})[0]
            y = year.string[0:4]
            print y

            g = ""
            genres = soup.findAll('div',{'itemprop':'genre'})
            for genre in genres:
                g+=str(genre.string) + ', '
            print g 
        
            d = ""
            directors = soup.findAll('dd',{'itemprop':'director'})
            for director in directors:
                d+=str(director.string) + ', '
            print d 
            
            a = ""
            actors = soup.findAll('dd',{'itemprop':'actor'})
            for actor in actors:
                a+= str(actor.string) + ', '
            print a 
        
            rating = soup.findAll('span',{'class':'value'})[0]
            print rating.string  
            
            scores = soup.findAll('span',{'class':'rating'})
            for score in scores:
                s = score.string.replace('stars', '').strip()
                print s  
        
            movie = Movie(urlid=number, title=title.string, descr=desc, year=y, genre=g, 
                          director=d, actor=a, rated=rating.string, rating=s, date_created=datetime.now())
            movie.save()
                
            #pause till next call to avoid being blocked!
            time.sleep(randint(10,30)) # from x to y seconds
        except Exception, e:
            print e
            time.sleep(randint(10,30)) # from x to y seconds
            continue
    return HttpResponse("success " + str(number))      