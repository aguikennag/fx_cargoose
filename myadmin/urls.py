from django.urls import path

from . import views,shipment


urlpatterns = [
    path("",views.Index.as_view(),name = "myadmin-index"),

    #shipment
    path("shipment/create/",shipment.CreateShipment.as_view(),name = 'create-shipment')
   
]