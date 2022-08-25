from django.urls import path, include

from main import views


urlpatterns = [
    path('', views.index),
    path('staff/', views.staff, name='staff'),
    path('update-staff/<int:pk>', views.update_staff, name='update-staff'),
    path('delete-staff/<int:pk>', views.delete_staff, name='delete-staff'),
    path('deliverer/', views.deliverer, name='deliverer'),
    path('update-deliverer/<int:pk>', views.update_deliverer, name='update-deliverer'),
    path('offers/', views.offer, name='offer'),
    path('update-offer/<int:pk>', views.update_offer, name='update-offer'),
    path('complaint/', views.complaint, name='complaint'),
    path("complaint/<int:id>", views.filter_complaint, name="filter-complaint"),
    path("offers/<int:id>", views.filter_offer, name="filter-offer"),
    path('products/', views.products, name='products'),
    path('update-product/<int:pk>', views.update_product, name='update-product'),
    path('delete-product/<int:pk>', views.delete_product, name='delete-product'),
    path('category/', views.category, name='category'),
    path('poll/', views.poll, name='poll'),
    path('delete-poll/<int:pk>', views.delete_poll, name='delete-poll'),
    path('ads/', views.ads, name='ads'),
    path('photos/', views.photos, name='photos'),
]
