import io,csv

from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django_tables2.tables import Table
import pandas as pd
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.

def index(request):
    context = {'a': 'Hello World'}
    return render(request, 'index.html', context)


def predictStockPrice(request):
    template = 'index.html'
    if request.method == 'GET':
        return render(request, template)
    else:
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        data = pd.read_csv(csv_file)
        data_html = data.to_html()
        context = {'df_table': data_html}
        return render(request, template, context)

