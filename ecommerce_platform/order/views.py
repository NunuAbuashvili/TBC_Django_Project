from django.shortcuts import render
from django.http import HttpResponse


def order_page_view(request):
    return HttpResponse("Welcome to the Order page!")

def order_history(request):
    return HttpResponse("Here is your order history!")
