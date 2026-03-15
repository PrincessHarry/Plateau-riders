from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.create_waybill, name='create_waybill'),
    path('track/', views.track_parcel, name='track_parcel'),
    path('receipt/<str:tracking_code>/', views.waybill_receipt, name='waybill_receipt'),
    path('list/', views.waybill_list, name='waybill_list'),
    path('<int:pk>/update-status/', views.update_waybill_status, name='update_waybill_status'),
]
