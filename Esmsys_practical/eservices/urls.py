from django.urls import path
from . import views

urlpatterns = [
    path('get-all-data/', views.get_all_data, name='get_all_data'),
    path('add-entry/', views.add_entry, name='add_entry'),
    path('delete-entry/<str:entry_type>/<int:id>/', views.delete_entry, name='delete_entry'),
]