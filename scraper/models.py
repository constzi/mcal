from django.db import models

class Movie(models.Model):
    urlid = models.IntegerField(max_length=20, default=0)
    title = models.CharField(max_length=1000)
    descr = models.TextField() 
    year = models.IntegerField(max_length=4, default=1900)
    genre = models.CharField(max_length=1000)
    director = models.CharField(max_length=1000)
    actor = models.CharField(max_length=1000)
    rated = models.CharField(max_length=10)
    rating = models.DecimalField(max_digits=5,decimal_places=1,default=1)  
    date_created = models.DateTimeField('date_published')
    def __unicode__(self):
        return self.title
    
