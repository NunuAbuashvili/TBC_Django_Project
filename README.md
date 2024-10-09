# Django E-commerce Project

## Overview
This is a basic Django-based e-commerce project designed for managing products
and orders in a store. It includes a **Store** app for handling products and categories,
and an **Order** app for managing customer orders. This project is currently in its initial stage 
and will be expanded over time with more features.


## Project Structure
The project consists of two main apps:

- **Store App**: Manages products, categories, and associated functionality.
- **Order App**: Manages customer orders and the ordering process.


## Current Features

### Store app
- Product and Category Models:
  - Products can belong to multiple categories.
  - Categories are organized hierarchically, allowing for nested subcategories.
  - Each product has a name, price, stock quantity, and an optional image.
- Admin Panel Configuration:
   - Categories and products are manageable via the Django admin interface, including hierarchical category management.
- Views:
   - `store_homepage`: Displays a simple homepage message.
   - `list_products`: Returns JSON data for all products, including category info.
   - `list_categories`: Returns JSON data for all categories, including top-level parent information.

### Order App
- The Order app structure is set up, with plans for managing customer orders.


## Future Plans
This project is a work in progress. Future updates will include enhanced functionality and design.


## Setup

1. Clone the repository.
2. Install the required packages:
    ```bash
   pip install -r requirements.txt
3. Run migrations: 
    ```bash
    python manage.py migrate
4. Create a superuser for accessing the admin panel: 
   ```bash
   python manage.py createsuperuser
5. Run the development server: 
   ```bash
   python manage.py runserver


## API Endpoints
- `/products/`: Returns a JSON list of products with category details.
- `/categories/`: Returns a JSON list of categories, including each top-level parent category.

## Contributing
This project is part of a learning process. While contributions are welcome, 
please note that major changes may be implemented as part of the learning journey.


## Note
This README is in its initial state and will be updated regularly as the project evolves. 
Check back for the latest information on features and usage.

*Last updated: [10.10.2024]*