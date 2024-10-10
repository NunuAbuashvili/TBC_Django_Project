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
    including id, categories, price, image URL, stock, creation, and update timestamps.

    @param request: The HTTP request object.
    @return: JSON containing product information.
    """
    products = Product.objects.all()
    data = []

    for item in products:
        data.append({
            'id': item.id,
            'name': item.name,
            'price': item.price,
            'stock_quantity': item.stock_quantity,
            'image_url': str(item.image),
            'time_of_creation': item.created_at,
            'time_of_update': item.updated_at,
            'active_status': item.is_active,
            'categories': [{'id': cat.id, 'name': cat.name} for cat in item.categories.all()],
        })

    return JsonResponse(data, safe=False, json_dumps_params={'indent': 2})


def show_categories(request: HttpRequest) -> JsonResponse:
    """
    Return a JSON response with a list of categories and their details,
    including their id, parent, description, and timestamps.

    @param request: The HTTP request object.
    @return: JSON containing category information.
    """
    categories = Category.objects.all()

    data = []

    for category in categories:
        data.append({
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'time_of_creation': category.created_at,
            'time_of_update': category.updated_at,
            'active_status': category.is_active,
            'parent_category': {
                'id': category.parent.id,
                'name': category.parent.name,
            } if category.parent else None,
        })

    return JsonResponse(data, safe=False, json_dumps_params={'indent': 2})
