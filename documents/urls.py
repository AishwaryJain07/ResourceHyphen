from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('add-file/', views.AddFileView.as_view(), name='add_file'),
    path('card-settings/', views.CardSettingsView.as_view(), name='card_settings'),
    path('view-pdf/<int:document_id>/', views.view_pdf, name='view_pdf'),
    path('download-pdf/<int:document_id>/', views.download_pdf, name='download_pdf'),
    path('delete-pdf/<int:document_id>/', views.delete_pdf, name='delete_pdf'),
    path('delete-subcard/<int:parent_id>/<int:subcard_id>/', views.delete_subcard, name='delete_subcard'),

]