from email.policy import default
from django.utils import timezone
from django.db import models
from django.contrib.auth.models   import AbstractUser
from django.utils.text import  slugify
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import os
import random




class Country(models.Model) :
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=50)

    def __str__(self) :
        return "{}({})".format(self.name,self.short_name)




class User(AbstractUser) :

    def get_path(instance,filename) :
        filename = "{}.{}".format(instance.name,filename.split('.')[1])
        return "users/dp/{}".format(filename)
    
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length = 50,blank = False,null = False)
    picture = models.FileField(upload_to = get_path)
   

    class Meta() :
        ordering = ['date_joined']

    def __init__(self,*args,**kwargs) :
        super(User,self).__init__(*args,**kwargs)
        #specify fields to monitor
        self.__fields_to_watch_for_changes = ['email'] 
        #set the old values
        for field in self.__fields_to_watch_for_changes :
            setattr(self,'__initial_{}'.format(field),getattr(self,field)) 



 

    @property
    def unique_id(self) :
        return "NTDID{}".format(self.pk)

    @property
    def get_picture(self) :
        BASE_DIR = settings.STATIC_URL
        default_path = os.path.join(BASE_DIR,"user-dashboard/images/user-thumb-sm.png")
        if not self.picture :
            return default_path
        
        return self.picture.url  

    def has_changed(self,field) :
        original = "__initial_{}".format(field) 
        return getattr(self,original)  == getattr(self,field)            

    def __str__(self)  :
        return self.username

    def save(self,*args,**kwargs) :
       
        #check if email changed 
        if self.has_changed('email') :
            self.email_verified = False
        self.slug = slugify(self.name) 
        super(User,self).save(*args,**kwargs)

    class Meta() :
        ordering = ['-date_joined']    


class Security(models.Model) :
    user = models.OneToOneField(get_user_model(),related_name ='security',on_delete = models.CASCADE)
    otp = models.PositiveIntegerField(blank=True,null = True)
    otp_expiry = models.DateTimeField(blank=True,null = True)


class Dashboard(models.Model) :
    last_checked = models.DateTimeField()


class Settings(models.Model) :
    user = models.OneToOneField(get_user_model(),related_name='settings',on_delete = models.CASCADE)
    email_on_transaction = models.BooleanField(default=True)
    password_on_withdrawal =  models.BooleanField(default=True)

    def __str__(self) :
        return "{}-setting".format(self.user.username)




class Notification(models.Model) :
    user = models.ForeignKey(User,related_name = 'notification',on_delete = models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add = True)

    class Meta() :
        ordering = ['-date']


class NewsLaterSubscriber(models.Model) :
    user = models.ForeignKey(User,related_name = 'news_subscibers',on_delete = models.CASCADE)

    def __str__(self)  :
        return self.email




