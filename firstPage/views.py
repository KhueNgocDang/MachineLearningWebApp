import json

import pandas as pd
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from template import *
from .forms import *

# Create your views here.
from .lr_prediction import lr_prediction, fetch_csv
from .models import StockInfo


def index(request):
    # companies = [obj.ticker for obj in Company.objects.all()]
    form = CompanyForm(request.POST, initial=0)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

    context = {'form': CompanyForm(request.POST)}

    return render(request, 'index.html', context)


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def predictStockPriceFromDataBase(request):
    symbol = request.GET['Company']
    data = fetch_csv(symbol)
    out = lr_prediction(data)

    return Response({'data': out}, template_name='predict_chart.html')


@api_view(('POST',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def predictStockPriceFromUpload(request):
    stock = request.FILES['file'].file
    df = pd.read_csv(stock)
    out = lr_prediction(df)

    return Response({'data': out}, template_name='predict_chart.html')
