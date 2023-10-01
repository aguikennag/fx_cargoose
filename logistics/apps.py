from django.apps import AppConfig
from django.core.signals import request_finished



class LogisticsConfig(AppConfig):
    name = 'logistics'

    def ready(self) :
        from . import signals
        from .models  import Shipment
        request_finished.connect(signals.shipment_on_create, sender= Shipment)    
        request_finished.connect(signals.shipment_on_transit_update, sender= Shipment)  
        request_finished.connect(signals.shipment_on_status_update, sender= Shipment)  



