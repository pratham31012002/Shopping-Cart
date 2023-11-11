## Shopping Cart RESTful API

An API for a e-commerce application created using the Django Rest Framework that allows the following functionality:

- Allows admins to add, remove and modify items(with name, description and price) to the product catalogue
- Allows users to create accounts (currently without authorization), create carts, view items in their cart, add items to their, modify their cart, and get the total cost of items in the cart

## Prerequisites
- Docker and docker-compose

## Building and Running the Application

Run the following command to build the image:

```
docker-compose build
```

Run the following command to run the application:

```
docker-compose up
```

Access the API at `http://127.0.0.1:8000/` to manage users, items, carts, and cart items.

## Running all tests

Run the following command:

```
docker-compose run web python manage.py test --verbosity 2
```

## API Endpoints

- **Get all users:**

  `GET /api/users/`

- **Get all items:**

  `GET /api/admin/items/`

- **Get all carts with their total costs:**

  `GET /api/carts/`

- **Get all cart items:**

  `GET /api/cartitems/`

- **Get total cost for a cart:**

  `GET /api/carts/<cart_id>/total_cost/`

- **Get available items for users:**

  `GET /api/users/available_items/`

- **Get cart id of a user:**

  `GET /api/carts/cart_id/?user=<user_id>`

- **Get all cart details of a user:**

  `GET /api/carts/?user=<user_id>`

- **Get all cart items of a user:**

  `GET /api/cartitems/?user=<user_id>`

- **Get all cart items of a cart:**

  `GET /api/cartitems/?cart=<cart_id>`

- **Get user details of user with given user id**
  
  `GET /api/users/<user_id>/`

- **Get item details of item with given item id**
  
  `GET /api/admin/items/<item_id>/`

- **Get cart details of cart with given cart id**
  
  `GET /api/carts/<cart_id>/`

- **Get cart item details of cart item with given cart item id**
  
  `GET /api/cartitems/<cart_item_id>/`

- **Create a new user:**
  
  `POST /api/users/`

  Request Body:

  ```json
  {
    "username": "newuser",
    "password": "newpassword"
  }
  ```

- **Create a new item:**

  `POST /api/admin/items/`

  Request Body:

  ```json
  {
    "name": "New Item",
    "description": "Description of the new item",
    "price": 29.99
  }
  ```

- **Create a new cart:**

  Note: 
    - A new cart needs to be created for each user in order to add items to that user's cart.
    - Each user can have either 0 or 1 cart.

  `POST /api/users/`

  Request Body:

  ```json
  {
    "user": "<user_id>"
  }
  ```

- **Create a new cart item using cart id:**

  `POST /api/cartitems/`

  Request Body:

  ```json
  {
    "cart": "<cart_id>",
    "item": "<item_id>",
    "quantity": 5
  }
  ```

- **Create a new cart item using user id:**

  `POST /api/cartitems/`

  Request Body:

  ```json
  {
    "user": "<user_id>",
    "item": "<item_id>",
    "quantity": 5
  }
  ```
- **Update all fields of an existing user:**

  `PUT /api/users/<user_id>/`

  Request Body:

  ```json
  {
    "username": "Updated username",
    "password": "Updated password"
  }
  ```

- **Update specific fields of an existing user:**

  `PATCH /api/users/<user_id>/`

  Request Body:

  ```json
  {
    "username": "Updated username",
  }
  ```

- **Update all fields of an existing item:**

  `PUT /api/admin/items/<item_id>/`

  Request Body:

  ```json
  {
    "name": "Updated Item",
    "description": "Updated description",
    "price": 39.99
  }
  ```

- **Update specific fields of an existing item:**

  `PATCH /api/admin/items/<item_id>/`

  Request Body:

  ```json
  {
    "name": "Updated Item",
  }
  ```

- **Update specific fields of an existing cart item:**
  `PATCH /api/cartitems/<cart_item_id>/`

  Request Body:

  ```json
  {
    "quantity": 5,
  }
  ```

- **Delete a user:**
  
  `DELETE /api/users/<user_id>/`

- **Delete an item:**

  `DELETE /api/admin/items/<item_id>/`

- **Delete a cart:**
  
  `DELETE /api/carts/<cart_id>/`

- **Delete a cart item:**
  
  `DELETE /api/cartitems/<cart_item_id>/`
