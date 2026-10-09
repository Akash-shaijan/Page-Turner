from django.db import models

# Create your models here.

import uuid

from django.contrib.auth.models import User



class BaseClass(models.Model):
    
    uuid=models.UUIDField(unique=True,default=uuid.uuid4)
    
    active_status=models.BooleanField(default=True)
    
    created_at=models.DateTimeField(auto_now_add=True)
    
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        
        abstract=True
        
# model for language
class Language(BaseClass):
    
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        
        verbose_name = 'Language'
        
        verbose_name_plural = 'Languages'

    def __str__(self):
        
        return self.name


# model for author
class Author(BaseClass):
    
    name = models.CharField(max_length=50, unique=True)
    
    photo = models.ImageField(upload_to='author-images/',blank=True,null=True)

    class Meta:
        
        verbose_name = 'Author'
        
        verbose_name_plural = 'Authors'

    def __str__(self):
        
        return self.name


# model for genre
class Genre(BaseClass):
    
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        
        verbose_name = 'Genre'
        
        verbose_name_plural = 'Genres'

    def __str__(self):
        
        return self.name


class Book(BaseClass):

    title = models.CharField(max_length=200)

    author = models.ForeignKey(Author,on_delete=models.CASCADE,related_name='books')

    genres = models.ManyToManyField(Genre,related_name='books')

    language = models.ForeignKey(Language,on_delete=models.SET_NULL,null=True,related_name='books')

    description = models.TextField(blank=True)

    has_digital = models.BooleanField(default=False)
    
    digital_file = models.FileField(upload_to='ebooks/',blank=True,null=True)

    has_physical = models.BooleanField(default=True)
    
    total_copies = models.PositiveIntegerField(default=0)
    
    available_copies = models.PositiveIntegerField(default=0)

    cover_image = models.ImageField(upload_to='book_covers/')

    class Meta:
        
        verbose_name = 'Book'
        
        verbose_name_plural = 'Books'

    def __str__(self):
        
        return self.title
    
    
    






