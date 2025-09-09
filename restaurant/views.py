from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RestaurantInfo , staff, MenuItem, Customer, Order
from .serializers import RestaurantSerializer, MenuItemSerializer, CustomerSerializer,OrderSerializer


# Create your views here.
def home(request):
    return HttpResponse("hello Django!")


# APIs for restaurant model
@api_view(['POST'])   #create new restaurant
def create_restaurant(request):
    serializer=RestaurantSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])   #list all restaurant
def list_restaurants(request):
    restaurant=RestaurantInfo.objects.all()
    serializer=RestaurantSerializer(restaurant,many=True)
    return Response(serializer.data)


@api_view(['GET'])    # view 1 restaurant by id
def get_restaurant(request,pk):
    try:
        restaurant=RestaurantInfo.objects.get(pk=pk)
    except RestaurantInfo.DoesNotExist:
        return Response({'error':'Restaurant not found'},status=status.HTTP_404_NOT_FOUND)
    serializer=RestaurantSerializer(restaurant)
    return Response(serializer.data)


@api_view(['PUT'])    # update restaurant info
def update_restaurant(request,pk):
    try:
        restaurant=RestaurantInfo.objects.get(pk=pk)
    except RestaurantInfo.DoesNotExist:
        return Response({'error':'Restaurant not found'},status=status.HTTP_404_NOT_FOUND)
    serializer=RestaurantSerializer(restaurant,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])    # to delete any record
def delete_restaurant(request,pk):
    try:
        restaurant=RestaurantInfo.objects.get(pk=pk)
    except RestaurantInfo.DoesNotExist:
        return Response({'error':'Restaurant Not Found'},status=status.HTTP_404_NOT_FOUND)
    restaurant.delete()
    return Response({'message':'data deleted successfully'},status=status.HTTP_204_NO_CONTENT)


# login API for staff model:
@api_view(['POST'])
def staff_login(request):
    email=request.data.get('email')
    password=request.data.get('password')
    try:
        staff_user=staff.objects.get(email=email)
    except staff.DoesNotExist:
        return Response({'Error':'Invalid Email'},status=status.HTTP_404_NOT_FOUND)
    if check_password(password,staff_user.password):
        return Response({"message":"Login successfull"},status=status.HTTP_200_OK)
    else:
        return Response({'Error':'Invalid password'},status=status.HTTP_401_UNAUTHORIZED)
    


# Menu item APIs- CURD Creation for MenuItem model:
# add new Menu:
@api_view(['POST'])
def create_menu_item(request):
    serializer=MenuItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# list all items
@api_view(['GET'])
def list_menu_item(request):
    items=MenuItem.objects.all()
    serializer=MenuItemSerializer(items,many=True)
    return Response(serializer.data)

# list 1 item
@api_view(['GET'])
def get_menu_item(request,pk):
    try:
        items=MenuItem.objects.get(pk=pk)
    except MenuItem.DoesNotExist:
        return Response({'error':'Item Does Not Found'},status=status.HTTP_404_NOT_FOUND)
    serializer=MenuItemSerializer(items)
    return Response(serializer.data)

# update data
@api_view(['PUT'])
def update_menu_item(request,pk):
    try:
        items=MenuItem.objects.get(pk=pk)
    except MenuItem.DoesNotExist:
        return Response({'error':'item not found'},status=status.HTTP_404_NOT_FOUND)
    serializer=MenuItemSerializer(items, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# DELETE DATA:
@api_view(['DELETE'])
def delete_menu_item(request,pk):
    try:
        items=MenuItem.objects.get(pk=pk)
    except MenuItem.DoesNotExist:
        return Response({'error':'item does not found'},status=status.HTTP_404_NOT_FOUND)
    items.delete()
    return Response({'message':'Data deleted successfully'},status=status.HTTP_204_NO_CONTENT)


class CustomerListCreateView(APIView):
    def get(self, request):
        customers=Customer.objects.all()
        serializer=CustomerSerializer(customers,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        serializer= CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

# order creation
class CreateOrderView(APIView):
    def post(self,request):
        total_price=request.data.get('total_price')
        customer_data=request.data.get('customer',{})
        
        # handles customer creation for guest
        if request.user.is_authenticated:
            customer=None
            user=request.user
        else:
            if customer_data:
                customer_serializer=CustomerSerializer(data=customer_data)
                if customer_serializer.is_valid():
                    customer=customer_serializer.save()
                else:
                    return Response({'error':'Invalid customer data','detail':customer_serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            else:
                customer=None
            user=None

        # if not request.user.is_authenticated:
        #     customer_serializer=CustomerSerializer(data=customer_data)
        #     if customer_serializer.is_valid():
        #         customer=customer_serializer.save()
        #     else:
        #         return Response({'error':'Invalid customer data','detail':customer_serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        #     user=None
        # else:
        #     customer=None
        #     user=request.user
        
        # create the order
        order=Order.objects.create(customer=customer,user=user,total_price=total_price)

        response_data={
            'order_id':order.id,
            'status':'success',
            'customer':CustomerSerializer(customer).data if customer else None
        }
        return Response(response_data,status=status.HTTP_201_CREATED)


# order history list
class CustomerOrderListView(APIView):
    def get(self,request):
        user=request.user
        customer_id=request.query_params.get('customer_id')
        if user.is_authenticated:
            orders=Order.objects.filter(user=user).order_by('-created_at')
        elif customer_id:
            orders=Order.objects.filter(customer_id=customer_id).order_by('-created_at')
        else:
            return Response({'detail':'user or customer required'},status=status.HTTP_400_BAD_REQUEST)
        serializer= OrderSerializer(orders,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)