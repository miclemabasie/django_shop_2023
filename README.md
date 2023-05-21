- [Django Online Shop](#django-online-shop)
- [Managing Payments and Orders](#managing-payments-and-orders)
- [Adding more advanced features](#adding-more-advanced-features)
  - [How the coupon system works](#how-the-coupon-system-works)
  - [Steps to add translation into a django project](#steps-to-add-translation-into-a-django-project)
  - [How Django determines the current language](#how-django-determines-the-current-language)

# Django Online Shop
  * Create a product catalog
  * Build a shopping cart useing Django sessions
  * Create custome contxt processors
  * Manage customer orders
  * Configure Celery in the project with RabbitMQ as a message broker
  * Send asynchronous notifications to customers using Celery
  * Monitor Celery using Flower

# Managing Payments and Orders
  * Intergate a payment gateway into your project
  * Export orders to CSV files
  * Create custom views for the administration site
  * Generate PDF invoices dynamically on order completion

# Adding more advanced features
  * Creating a coupon system to apply discounts
  * Adding internationalization to your project
  * Using Rosetta to manage transactions
  * Translating models using django-parler
  * Building a product recommendation engine

## How the coupon system works
  1. The User adds products to the shopping cart.
  2. The user can enter a coupon code in a form displayed on the shopping cart detail page
  3. When the user enters a coupon code and submits the form, we look for an existing coupon with the code that is currently valid. we check that the code matches the one entered by the user, that the active attribute of the code is True, and that the current datetime is between the valid_from and valid_to values
  4. If a coupon is found, we save it in the user's session and display the cart, including the discount applied tot it and the updated total amount.
  5. When the user places an order, you save the coupon to the given order

## Steps to add translation into a django project
  1. Mark strings for translation in your Python code and your templates
  2. Run the ```makemessages``` command to create or update message files that include all translation strings from your code
  3. Translate the strings contained in the message file and compile them using the  ```compilemessages``` management command
   
## How Django determines the current language
  1. If you are using ```i18n_patterns```, that is, you are using translation URL patterns, it looks for language prefix in the requested URL to determine the current language.
  2. If no language prefix is found, it looks for an existing ```LANGUAGE_SESSION_KEY``` in the current session.
  3. If the language is not set in the session, it looks for an exisiting cookie with the current language. A custom name for this cookie can be provided in the ```LANGUAGE_NAME``` setting. By default, the name for this cookie is ```django_language```.
  4. If no cookie is found, it looks for the ```Accept-Language``` HTTP header of the request.
  5. If the ```Accept-Language``` header does not specify a language, Django uses the language defined in the ```LANAGUAGE_CODE``` settings.