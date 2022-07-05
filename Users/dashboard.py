
from django.shortcuts import render
from django.views.generic import ListView,View,RedirectView,TemplateView
from django.views.generic.edit import CreateView,UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.forms.models import model_to_dict
from django.db.models import Sum

from django.http import JsonResponse,HttpResponse


class Dashboard(LoginRequiredMixin,TemplateView) :
    template_name = 'dashboard.html'

    def get_context_data(self,*args,**kwargs) :
     
        ctx = super(Dashboard,self).get_context_data(*args,**kwargs) 

        return ctx

    def get(self,request,*args,**kwargs)   :
    
        return render(request,self.template_name,self.get_context_data())    




