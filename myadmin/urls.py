from django.urls import path

from . import views,shipment


urlpatterns = [
    path("",views.Index.as_view(),name = "myadmin-index"),

    #shipment
    path("shipment/create/",shipment.CreateShipment.as_view(),name = 'create-shipment'),
    path("shipments/",shipment.Shipments.as_view(),name = "shipments"),
    
    path("shipment/detail/<str:tracking_number>/update-status-log/<str:action>/",shipment.UpdateStatusLog.as_view(),name = "update-status-log"),
    
    #path("shipment/detail/<str:tracking_number>/add-status-log/",shipment.AddStatusLog.as_view(),name = "add-status-log"),
    #path("shipment/detail/<str:tracking_number>/add-transit-log/",shipment.AddTransitLog.as_view(),name = "add-transit-log"),
   
]