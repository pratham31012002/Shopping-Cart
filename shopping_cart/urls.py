from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, CartViewSet, CartItemViewSet, UserViewSet

router = DefaultRouter()
router.register(r'admin/items', ItemViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cartitems', CartItemViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]