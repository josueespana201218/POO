from contacts import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ContactListView.as_view(), name='contact_list'),
    path('new', views.ContactCreateView.as_view(), name='contact_new'),
    path('<int:pk>/', views.ContactDetailView.as_view(), name='contact_detail'),
    path('<int:pk>/edit/', views.ContactUpdateView.as_view(), name='contact_edit'),
    path('<int:pk>/delete/', views.ContactDeleteView.as_view(), name='contact_delete'),
    path('contact/<int:pk>/toggle-favorite/', views.ContactToggleFavoriteView.as_view(), name='contact_toggle_favorite'),
]
