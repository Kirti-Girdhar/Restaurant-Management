from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.contrib.auth import get_user_model

# Create your models here.


class RestaurantInfo(models.Model):
    name=models.CharField(max_length=100)
    owner_name=models.CharField(max_length=70)
    email=models.EmailField(unique=True)
    phone_number=models.CharField(max_length=20)
    address=models.TextField(max_length=200)
    city=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    restaurant=models.ForeignKey(RestaurantInfo, on_delete=models.CASCADE, related_name='menu_items')
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=8,decimal_places=2)
    is_available=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - Rs. {self.price}'
    

# Staff model:
class StaffManager(BaseUserManager):
    def create_user(self,email,name,password=None,restaurant=None):
        if not email:
            raise ValueError("Email is required! ")
        user=self.model(email=self.normalize_email(email),name=name,restaurant=restaurant)
        user.set_password(password)
        user.save(using=self._db)
        return user

class staff(AbstractBaseUser):
    email=models.EmailField(unique=True)
    name=models.CharField(max_length=50)
    restaurant=models.ForeignKey(RestaurantInfo, on_delete=models.CASCADE,related_name='staff_members')
    is_active=models.BooleanField(default=True)

    USERNAME_FIELD='email'

    objects=StaffManager()

    def __str__(self):
        return f"{self.name}-({self.email})"


# Customer model for dine-in
class Customer(models.Model):
    name=models.CharField(max_length=100,blank=True,null=True)
    phone=models.CharField(max_length=20,blank=True,null=True)
    email=models.EmailField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.name:
            return self.name
        elif self.phone:
            return f"Guest Mob({self.phone})"
        elif self.email:
            return f'Guest Mail({self.email})'
        return "Anonymous Customer"
    

# order model: for logged in user
User= get_user_model()
class Order(models.Model):
    customer =models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True, blank=True)
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    total_price=models.DecimalField(max_digits=8,decimal_places=2)
    status=models.CharField(max_length=20, default="pending")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'order no. {self.id} - Rs. {self.total_price} - status {self.status}'\
        