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

class CreateItemTest(BaseViewTest):
    def test_create_item(self):
        """
        Ensure we can create a new item
        """
        url = reverse('item-list')
        data = {'name': 'New Item', 'description': 'New Description', 'price': 30.0}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 3)

class UpdateItemTest(BaseViewTest):
    def test_update_item(self):
        """
        Ensure we can update an existing item
        """
        url = reverse('item-detail', kwargs={'pk': self.item1.id})
        data = {'name': 'Updated Item', 'description': 'Updated Description', 'price': 40.0}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item1.refresh_from_db()
        self.assertEqual(self.item1.name, 'Updated Item')
        self.assertEqual(self.item1.description, 'Updated Description')
        self.assertEqual(self.item1.price, 40.0)

class PatchItemTest(BaseViewTest):
    def test_patch_item(self):
        """
        Ensure we can patch an existing item
        """
        url = reverse('item-detail', kwargs={'pk': self.item1.id})
        data = {'price': 50.0}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item1.refresh_from_db()
        self.assertEqual(self.item1.price, 50.0)

class DeleteItemTest(BaseViewTest):
    def test_delete_item(self):
        """
        Ensure we can delete an existing item
        """
        url = reverse('item-detail', kwargs={'pk': self.item1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 1)

        item1_found = Item.objects.all().filter(id = self.item1.id)
        self.assertEqual(item1_found.count(), 0)

class CreateUserTest(BaseViewTest):
    def test_create_user(self):
        """
        Ensure we can create a new user
        """
        url = reverse('user-list')
        data = {'username': 'newuser', 'password': 'newpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        new_user_found = User.objects.all().filter(username='newuser')
        self.assertEqual(new_user_found.count(), 1)

class UpdateUserTest(BaseViewTest):
    def test_update_user(self):
        """
        Ensure we can update an existing user
        """
        url = reverse('user-detail', kwargs={'pk': self.user1.id})
        data = {'username': 'updateduser', 'password': 'updatedpassword'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, 'updateduser')
        self.assertEqual(self.user1.password, 'updatedpassword')

class PatchUserTest(BaseViewTest):
    def test_patch_user(self):
        """
        Ensure we can patch an existing user
        """
        url = reverse('user-detail', kwargs={'pk': self.user1.id})
        data = {'username': 'newusername'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, 'newusername')

class DeleteUserTest(BaseViewTest):
    def test_delete_user(self):
        """
        Ensure we can delete an existing user
        """
        url = reverse('user-detail', kwargs={'pk': self.user1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)

        user1_found = User.objects.all().filter(id=self.user1.id)
        self.assertEqual(user1_found.count(), 0)

class CreateCartTest(BaseViewTest):
    def test_create_cart(self):
        """
        Ensure we can create a new cart
        """
        url = reverse('user-list')
        data = {'username': 'newuser', 'password': 'newpassword'}
        response = self.client.post(url, data, format='json')
        new_user_id = response.data['id']
        url = reverse('cart-list')
        data = {'user': new_user_id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.count(), 3)

class CreateCartItemTest(BaseViewTest):
    def test_create_cart_item_using_cart_id(self):
        """
        Ensure we can create a new cart item using cart_id
        """
        url = reverse('cartitem-list')
        data = {'cart': self.cart2.id, 'item': self.item2.id, 'quantity': 3}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.all().filter(cart=self.cart1).count(), 2)
        self.assertEqual(self.cart2.total_cost(), 110.0)

    def test_create_cart_item_using_user_id(self):
        """
        Ensure we can create a new cart item using user_id
        """
        item3 = self.create_item("item3", "description3", 25.0)
        url = reverse('cartitem-list')
        data = {'user': self.user1.id, 'item': item3.id, 'quantity': 3}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.all().filter(cart=self.cart1).count(), 3)
        self.assertEqual(CartItem.objects.all().filter(cart__user__id=self.user1.id).count(), 3)
        self.assertEqual(self.cart1.total_cost(), 125.0)

class PatchCartItemTest(BaseViewTest):
    def test_patch_cart_item(self):
        """
        Ensure we can patch an existing cart item
        """
        url = reverse('cartitem-detail', kwargs={'pk': self.cart1_item1.id})
        data = {'quantity': 5}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cart1_item1.refresh_from_db()
        self.assertEqual(self.cart1_item1.quantity, 5)

class DeleteCartItemTest(BaseViewTest):
    def test_delete_cart_item(self):
        """
        Ensure we can delete an existing cart item
        """
        url = reverse('cartitem-detail', kwargs={'pk': self.cart1_item1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CartItem.objects.all().filter(cart=self.cart1_item1.cart).count(), 1)

        cart1_item1_found = CartItem.objects.all().filter(id=self.cart1_item1.id)
        self.assertEqual(cart1_item1_found.count(), 0)
