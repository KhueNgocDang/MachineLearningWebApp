from import_export import resources
from .models import *


class CompanyResource(resources.ModelResource):
    class Meta:
        model = Company


class ExchangeResource(resources.ModelResource):
    class Meta:
        model = Exchange


class IndustryResource(resources.ModelResource):
    class Meta:
        model = Industry
