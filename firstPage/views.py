from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index(request):
    context = {'a': 'Hello World'}
    return render(request, 'index.html', context)


def predictStockPrice(request):
    context = {'a': 'Hello New World'}
    return render(request, 'index.html', context)
