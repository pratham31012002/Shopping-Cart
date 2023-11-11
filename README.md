**Shopping Cart RESTful API**

An API for a e-commerce application created using the Django Rest Framework that allows the following functionality:

- Allows admins to add, remove and modify items(with name, description and price) to the product catalogue
- Allows users to create accounts (currently without authorization), create carts, view items in their cart, add items to their, modify their cart, and get the total cost of items in the cart

**Prerequisites**
- Docker and docker-compose

**Building and Running the Application**

Run the following command to build the image:

```
docker-compose build
```

Run the following command to run the application:

```
docker-compose up
```

**Running all tests**

Run the following command:

```
docker-compose run web python manage.py test --verbosity 2
```