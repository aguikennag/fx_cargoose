from django.shortcuts import render
from django.views.generic import TemplateView,View,ListView,DetailView
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings

from .models import Blog


class BlogList(ListView) :
    template_name = 'blog-list.html'
    model = Blog
    context_object_name = 'blogs'
    blog_tags = [
    "Logistics",
    "Shipping",
    "Freight",
    "Supply Chain",
    "Transportation",
    "Cargo",
    "International Shipping",
    "Container Shipping",
    "Warehousing",
    "Port Operations",
    "Customs Clearance",
    "Maritime Industry",
    "E-commerce Logistics",
    "Last-Mile Delivery",
    "Cross-Border Shipping",
    "Inventory Management",
    "Cold Chain Logistics",
    "Sustainability",
    "Technology in Shipping",
    "Global Trade",
    "Shipping Regulations",
    "Customer Experience",
    "Trade Routes",
    "Supply Chain Optimization",
    "Air Freight",
    "Rail Freight",
    "Trucking",
    "Packaging",
    "Import and Export",
    "Risk Management",
]


    def get_context_data(self,*args,**kwargs) : 
        context = super(BlogList,self).get_context_data(*args,**kwargs) 
        context['latest_blog'] = self.model.objects.all()
        context['tags'] = self.blog_tags[:7]
        return context
        



class BlogDetail(DetailView) :
    template_name = 'blog-detail.html'
    model = Blog
    context_object_name = 'blog'

    def get_context_data(self,*args,**kwargs) : 
        context = super(BlogDetail,self).get_context_data(*args,**kwargs) 
        context['latest_blog'] = self.model.objects.all()
        context['tags'] = BlogList.blog_tags[:7]
        return context
