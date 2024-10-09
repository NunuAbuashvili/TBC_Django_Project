from typing import Optional
from itertools import product

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse

from .models import Product, Category


def store_homepage(request: HttpRequest) -> HttpResponse:
    """
    Display the homepage of the store.

    @param request: The HTTP request object.
    @return: A simple greeting message for the store homepage.
    """
    return HttpResponse('Welcome to the Store!')


def list_products(request: HttpRequest) -> JsonResponse:
    """
    Return a JSON response with a list of products and their details,
    including categories, price, stock, creation, and update timestamps.

    @param request: The HTTP request object.
    @return: JSON containing product information.
    """
    products = Product.objects.all()
    data = {}

    for index, item in enumerate(products, start=1):
        data[f'product {index}'] = {
            'name': item.name,
            'price': item.price,
            'stock_quantity': item.stock_quantity,
            'time_of_creation': item.created_at,
            'time_of_update': item.updated_at,
            'active_status': item.is_active,
            'categories': [{'id': cat.id, 'name': cat.name} for cat in item.categories.all()],
        }

    return JsonResponse(data, json_dumps_params={'indent': 2})


def show_categories(request: HttpRequest) -> JsonResponse:
    """
    Return a JSON response with a list of categories and their details,
    including their top-level parent, description, and timestamps.

    @param request: The HTTP request object.
    @return: JSON containing category information.
    """
    categories = Category.objects.all()

    def path_to_root_category(current_category: Category) -> Optional[Category]:
        """
        Find the top-level parent category for a given category.

        @param current_category: The Category instance for which to find the top-level parent.
        @return: The top-level parent category, or None if no parent exists.
        """
        if current_category.parent is None:
            return None
        parent = current_category.parent
        while parent.parent is not None:
            parent = parent.parent
        return parent

    data = {}

    for index, category in enumerate(categories, start=1):
        data[f'category {index}'] = {
            'name': category.name,
            'description': category.description,
            'time_of_creation': category.created_at,
            'time_of_update': category.updated_at,
            'active_status': category.is_active,
            'top_level_parent': {
                'id': path_to_root_category(category).id,
                'name': path_to_root_category(category).name,
            } if path_to_root_category(category) else 'None',
        }

    return JsonResponse(data, json_dumps_params={'indent': 2})
