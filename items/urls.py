from django.urls import path
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
    path('item/<int:pk>/change_amount', views.ItemActionCreateView.as_view(), name='create_item_action'),
    path('item/<int:pk>/add_amount', views.ItemActionAddCreateView.as_view(), name='create_item_action_add'),
    path('item/<int:pk>/move_amount', views.ItemActionMoveCreateView.as_view(), name='create_item_action_move'),
    path('item/<int:pk>/remove_amount', views.ItemActionRemoveCreateView.as_view(), name='create_item_action_remove'),
    path('item/<int:pk>', views.ItemDetailView.as_view(), name='view_item'),
    path('locations', views.LocationListView.as_view(), name='list_locations'),
    path('location/create', views.LocationCreateView.as_view(), name='create_location'),
    path('location/<int:pk>/edit', views.LocationEditView.as_view(), name='edit_location'),
    path('location/<int:pk>/delete', views.LocationDeleteView.as_view(), name='delete_location'),
    path('location/<int:pk>', views.LocationDetailView.as_view(), name='view_location'),
    path('categories', views.CategoryListView.as_view(), name='list_categories'),
    path('category/create', views.CategoryCreateView.as_view(), name='create_category'),
    path('category/<int:pk>/edit', views.CategoryEditView.as_view(), name='edit_category'),
    path('category/<int:pk>/delete', views.CategoryDeleteView.as_view(), name='delete_category'),
    path('category/<int:pk>', views.CategoryDetailView.as_view(), name='view_category'),
    path('item_types', views.ItemTypeListView.as_view(), name='list_item_types'),
    path('item_type/create', views.ItemTypeCreateView.as_view(), name='create_item_type'),
    path('item_type/<int:pk>/edit', views.ItemTypeEditView.as_view(), name='edit_item_type'),
    path('item_type/<int:pk>/delete', views.ItemTypeDeleteView.as_view(), name='delete_item_type'),
    path('item_type/<int:pk>', views.ItemTypeDetailView.as_view(), name='view_item_type'),
]

