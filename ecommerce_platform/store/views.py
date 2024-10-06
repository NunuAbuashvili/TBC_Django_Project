from django.shortcuts import render
from django.http import HttpResponse


def store_homepage(request):
    return HttpResponse('Welcome to the Store!')

def store_products(request):
    return HttpResponse("Here is a list of our products!")
