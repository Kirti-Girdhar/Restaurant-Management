from rest_framework import serializers
from . models import RestaurantInfo, MenuItem, Customer, Order

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model=RestaurantInfo
        fields='__all__'
        
    def validate_email(self,value):
        if "spam" in value:
            raise serializers.ValidationError("Invalid email domain.")
        return value


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=MenuItem
        fields='__all__'
        read_only_fields=['id','created_at']


class CustomerSerializer(serializers.ModelSerializer):
    name= serializers.CharField(required=False, allow_blank=True, allow_null=True)
    phone= serializers.CharField(required=False, allow_blank=True, allow_null=True)
    email= serializers.EmailField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model=Customer
        fields=['id','name','phone','email','created_at']
        read_only_fields=['id','created_at']


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model=Order
        fields='__all__'   # customer , user,total_price, status, created_at
        read_only_fields=['id','created_at']

    def get_customer_name(self, obj):
        if obj.customer and obj.customer.name:
            return obj.customer.name
        elif obj.user and obj.user.username:
            return obj.user.username
        return "Guest"
