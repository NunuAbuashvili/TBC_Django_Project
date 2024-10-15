from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count, Sum, Max, Min, Avg, F, Prefetch, Q, OuterRef, Subquery
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
            'image_url': item.image.url if item.image.url else None,
            'time_of_creation': item.created_at,
            'time_of_update': item.updated_at,
            'active_status': item.is_active,
            'categories': [{'id': cat.id, 'name': cat.name} for cat in item.categories.all()],
        })

    return JsonResponse(data, safe=False, json_dumps_params={'indent': 2})


def list_categories(request: HttpRequest) -> JsonResponse:
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


def categories_list_view(request: HttpRequest) -> HttpResponse:
    """
    Renders a list of root categories and the amount of their products.

    @param request: The HTTP request object.
    @return: The HTTP response with the rendered list of root categories and product amounts.
    """
    product_count_subquery = Product.objects.filter(
        Q(categories=OuterRef('pk')) |
        Q(categories__lft__gt=OuterRef('lft'),
          categories__rght__lt=OuterRef('rght'),
          categories__tree_id=OuterRef('tree_id'))
    ).values('categories__tree_id').annotate(
        product_count=Count('id', distinct=True)
    ).values('product_count')

    root_categories = Category.objects.root_nodes().annotate(
        total_products=Coalesce(Subquery(product_count_subquery), 0)
    )

    categories_data = [{
        'category': category,
        'total_products': category.total_products,
    } for category in root_categories]

    return render(request, "categories.html", {'categories': categories_data})


def category_detailed_view(request: HttpRequest, category_id: int) -> HttpResponse:
    """
    Renders the detailed view of a category, including products under the category tree,
    and statistics, e.g. most expensive product, cheapest product, average price,
    and total value of products

    @param request: The HTTP request object.
    @param category_id: The ID of the category to retrieve.
    @return: The HTTP response with the rendered category details, products, and statistics.
    """
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(
        categories__in=category.get_descendants()).distinct().annotate(
        total_value=F('price') * F('stock_quantity')
    )

    paginator = Paginator(products, 3)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    statistics = products.aggregate(
        category_total_value=Sum(F('price') * F('stock_quantity')),
        max_price=Max('price'),
        min_price=Min('price'),
        avg_price=Avg('price'),
        total_products=Count('id'),
    )

    context = {
        'category': category,
        'page_object': page_object,
        'statistics': statistics,
    }

    return render(request, 'category.html', context)


def product_detailed_view(request: HttpRequest, category_id: int, product_id: int) -> HttpResponse:
    """
    Renders the detailed view of a product.

    @param request: The HTTP request object.
    @param category_id: The ID of the root category associated with the product.
    @param product_id: The ID of the product to retrieve.
    @return: The HTTP response with the rendered product details.
    """
    category = get_object_or_404(Category.objects.only('id', 'name'), id=category_id)
    product = get_object_or_404(
        Product.objects.prefetch_related(
            Prefetch('categories', queryset=Category.objects.only('name')),
        ),
        id=product_id
    )
    product_categories = ', '.join(category.name for category in product.categories.all())
    context = {
        'product': product,
        'product_categories': product_categories,
        'category': category,
    }

    return render(request, 'product.html', context)
