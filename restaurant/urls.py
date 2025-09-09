from django.urls import path
from . import views
from .views import CustomerListCreateView,CreateOrderView,CustomerOrderListView

urlpatterns=[
    path('',views.home),
    path('restaurant/register/',views.create_restaurant,name='create_restaurant'),
    path('restaurants/',views.list_restaurants,name='list_restraunts'),
    path('restaurant/<int:pk>/',views.get_restaurant,name='get_restaurant'),
    path('restaurant/update/<int:pk>/',views.update_restaurant,name='update_restaurant'),
    path('restaurant/delete/<int:pk>/',views.delete_restaurant,name='delete_restaurant'),

    path('stafflogin/',views.staff_login,name='staff_login'),
    
    path('menuitem/createmenu/',views.create_menu_item,name='create_menu_item'),
    path('menuitems/',views.list_menu_item,name='list_menu_item'),
    path('menuitem/<int:pk>/',views.get_menu_item,name='get_menu_item'),
    path('menuitem/update/<int:pk>/',views.update_menu_item,name='update_menu_item'),
    path('menuitem/delete/<int:pk>',views.delete_menu_item,name='delete_menu_item'),
    path('customer/',CustomerListCreateView.as_view(),name='customer_list_create'),
    path('order/create/',CreateOrderView.as_view(),name='create_order'),
    path('orders/history/', CustomerOrderListView.as_view(),name='order_history'),
]

