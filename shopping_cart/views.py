from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Item, Cart, CartItem, User
from .serializers import ItemSerializer, CartSerializer, CartItemSerializer, UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False)
    def available_items(self, request):
        cart = Item.objects.all()
        data = ItemSerializer(cart, many=True).data
        return Response({'available_items': data})

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(detail=True)
    def total_cost(self, request, pk=None):
        cart = self.get_object()
        return Response({'total_cost': cart.total_cost()})
    
    @action(detail=False)
    def cart_id(self, request):
        user_id = request.query_params.get('user')
        if user_id is not None:
            try:
                user_cart = Cart.objects.get(user=user_id)
                return Response({'cart': user_cart.id})
            except:
                return Response({'error': [f"Invalid user '{user_id}' - user does not exist or user does not have an associated cart"]}, status=404)
        else:
            return Response({'error': 'user parameter required'}, status=400)

    
    def get_queryset(self):
        queryset = Cart.objects.all()
        user_id = self.request.query_params.get('user', None)
        if user_id is not None:
            queryset = queryset.filter(user__id = user_id)
        return queryset


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def create(self, request, *args, **kwargs):
        user_id = self.request.data.get('user', None)
        if user_id is not None:
            self.request.data.pop('user', None)
            try:
                cart = Cart.objects.get(user = user_id)
                self.request.data['cart'] = cart.id
            except:
                return Response({"error": [f"Invalid user '{user_id}' - user does not exist or user does not have an associated cart"]}, status=404)
        return super().create(request, args, kwargs)
    
    def get_queryset(self):
        queryset = CartItem.objects.all()
        user_id = self.request.query_params.get('user', None)
        if user_id is not None:
            queryset = queryset.filter(cart__user__id = user_id)
        cart_id = self.request.query_params.get('cart', None)
        if cart_id is not None:
            queryset = queryset.filter(cart__id = cart_id)
        return queryset
