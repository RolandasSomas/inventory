from django.urls import path, include
from . import views

app_name='items'
#
urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/profile/', views.profile, name='profile'),
    path('items', views.ItemsListView.as_view(), name='list_items'),
    path('item/create', views.ItemCreateView.as_view(), name='create_item'),
    path('item/<int:pk>/edit', views.ItemEditView.as_view(), name='edit_item'),
    path('item/<int:pk>/delete', views.ItemDeleteView.as_view(), name='delete_item'),
    path('item/<int:pk>', views.ItemDetailView.as_view(), name='view_item'),
]

