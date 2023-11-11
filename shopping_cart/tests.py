from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Item, Cart, CartItem
from .serializers import ItemSerializer, CartSerializer, CartItemSerializer, UserSerializer

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_item(name="", description="", price=0.0):
        if name != "" and description != "" and price != 0.0:
            return Item.objects.create(name=name, description=description, price=price)

    @staticmethod
    def create_user(username="", password=""):
        if username != "" and password != "":
            return User.objects.create_user(username=username, password=password)

    @staticmethod
    def create_cart(user=None):
        if user is not None:
            return Cart.objects.create(user=user)

    @staticmethod
    def create_cart_item(cart=None, item=None, quantity=1):
        if cart is not None and item is not None:
            return CartItem.objects.create(cart=cart, item=item, quantity=quantity)

    def setUp(self):
        # create a user
        self.user1 = self.create_user("testuser1", "testpassword1")
        self.user2 = self.create_user("testuser2", "testpassword2")

        # create items
        self.item1 = self.create_item("item1", "description1", 10.0)
        self.item2 = self.create_item("item2", "description2", 20.0)
        
        # create a cart for the user
        self.cart1 = self.create_cart(self.user1)
        self.cart2 = self.create_cart(self.user2)

        # add items to the cart
        self.cart1_item1 = self.create_cart_item(self.cart1, self.item1, 1)
        self.cart1_item2 = self.create_cart_item(self.cart1, self.item2, 2)

        self.cart2_item1 = self.create_cart_item(self.cart2, self.item1, 5)

class GetAllUsersTest(BaseViewTest):

    def test_get_all_users(self):
        """
        This test ensures that all users added in the setUp method
        exist when we make a GET request to the users/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(reverse("user-list"))
        # fetch the data from db
        expected = User.objects.all()
        serialized = UserSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetAllItemsTest(BaseViewTest):

    def test_get_all_items(self):
        """
        This test ensures that all items added in the setUp method
        exist when we make a GET request to the items/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(reverse("item-list"))
        # fetch the data from db
        expected = Item.objects.all()
        serialized = ItemSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetAllCartsTest(BaseViewTest):

    def test_get_all_carts(self):
        """
        This test ensures that all carts added in the setUp method
        exist when we make a GET request to the carts/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(reverse("cart-list"))
        # fetch the data from db
        expected = Cart.objects.all()
        serialized = CartSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetAllCartItemsTest(BaseViewTest):

    def test_get_all_cart_items(self):
        """
        This test ensures that all cart items added in the setUp method
        exist when we make a GET request to the cartitems/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(reverse("cartitem-list"))
        # fetch the data from db
        expected = CartItem.objects.all()
        serialized = CartItemSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_all_cart_items_user_given(self):
        """
        This test ensures that all cart items created in the setUp method
        exists for the given user when we make a GET request to the cartitems/ endpoint
        and provide the user id as parameter
        """
        response = self.client.get(f"{reverse('cartitem-list')}?user={self.user1.id}")
        expected = CartItem.objects.all().filter(cart__user__id=self.user1.id)
        serialized = CartItemSerializer(expected, many=True)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_cart_items_cart_given(self):
        """
        This test ensures that all cart items created in the setUp method
        exists for the given cart when we make a GET request to the cartitems/ endpoint
        and provide the cart id as parameter
        """
        response = self.client.get(f"{reverse('cartitem-list')}?cart={self.cart2.id}")
        expected = CartItem.objects.all().filter(cart__id=self.cart2.id)
        serialized = CartItemSerializer(expected, many=True)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetCartTest(BaseViewTest):

    def test_get_cart(self):
        """
        This test ensures that the cart created in the setUp method
        exists when we make a GET request to the carts/ endpoint
        """
        response = self.client.get(
            reverse("cart-detail", kwargs={"pk": self.cart1.id})
        )
        expected = Cart.objects.get(pk=self.cart1.id)
        serialized = CartSerializer(expected)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_cart_user_given(self):
        """
        This test ensures that the cart created in the setUp method
        exists when we make a GET request to the carts/ endpoint
        and provide the user id as parameter
        """
        response = self.client.get(f"{reverse('cart-list')}?user={self.user1.id}")
        expected = Cart.objects.get(pk=self.cart1.id)
        serialized = CartSerializer(expected)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetCartItemTest(BaseViewTest):

    def test_get_cart_item(self):
        """
        This test ensures that the cart item created in the setUp method
        exists when we make a GET request to the cartitems/ endpoint
        """
        response = self.client.get(
            reverse("cartitem-detail", kwargs={"pk": self.cart1_item1.id})
        )
        expected = CartItem.objects.get(pk=self.cart1_item1.id)
        serialized = CartItemSerializer(expected)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
class GetAllAvailableItemsForUsers(BaseViewTest):
    def test_get_all_available_items_for_users(self):
        """
        This test ensures that all available items for users are returned 
        by making a get request to the users/available_items endpoint
        """
        # hit the API endpoint
        response = self.client.get(f"{reverse('user-available-items')}")
        # fetch the data from db
        expected = Item.objects.all()
        serialized = ItemSerializer(expected, many=True)
        self.assertEqual(response.data['available_items'], serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetTotalCostForCart(BaseViewTest):
    def test_get_total_cost_for_cart(self):
        """
        This test ensures that total cost of a cart is correctly calculated
        """
        response = self.client.get(reverse("cart-total-cost", kwargs={"pk": self.cart1.id}))
        expected = 50.0
        self.assertEqual(response.data["total_cost"], expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse("cart-total-cost", kwargs={"pk": self.cart2.id}))
        expected = 50.0
        self.assertEqual(response.data["total_cost"], expected)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Add test classes for POST, PUT, PATCH and DELETE methods

