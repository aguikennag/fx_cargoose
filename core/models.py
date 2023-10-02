from django.db import models

from django.utils.text import slugify


class Country(models.Model) :
    name = models.CharField(max_length=20)
    short_name = models.CharField(max_length=5)

    def __str__(self) :
        return self.name
    


class Blog(models.Model) :
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,default="",blank=True)
    body = models.TextField()
    date = models.DateTimeField()
    img = models.FileField(upload_to="blog")
    

    @property
    def body_shortened(self) :
        return self.body[:100] + "..."
    

    @property
    def title_shortened(self) :
        return self.title[:50] + "..."
     
    def __str__(self) :
        return self.title

    def save(self, **kwargs):
        self.slug = slugify(self.title)
        super(Blog, self).save(**kwargs)
