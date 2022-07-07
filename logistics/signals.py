
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Shipment,StatusLog


@receiver(post_save, sender= Shipment)
def shipment_on_create(sender, instance, created, **kwargs):
    if  created :
        #send email that the shipment has been registered
        #create first status 
        StatusLog.objects.create(shipment = instance,status = "registered")
        
           
  
        
    


