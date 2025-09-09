from django.contrib import admin

# Register your models here.
# restaurant/admin.py
from .models import MenuItem, RestaurantInfo, staff, Customer,Order

admin.site.register(RestaurantInfo)
admin.site.register(MenuItem)
admin.site.register(staff)
admin.site.register(Customer)
admin.site.register(Order)