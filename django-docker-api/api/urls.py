from django.urls import path

from . import views

urlpatterns = [
    path('documento', views.get_documentos, name='get_documentos'),
    path('documento/<int:pk>', views.get_documento, name='get_documento'),
    path('documento/create', views.create_documento, name='create_documento'),
    path('documento/update/<int:pk>',
         views.update_documento, name='update_documento'),
    path('documento/delete/<int:pk>',
         views.delete_documento, name='delete_documento'),
]
