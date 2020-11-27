import io
from django import forms
from django.core.checks import messages
from django.http import request
from django.shortcuts import redirect
from import_export.forms import ImportForm, ConfirmImportForm

from firstPage.models import Exchange


class CustomImportForm(ImportForm):
    exchange = forms.ModelChoiceField(
        queryset=Exchange.objects.all(),
        required=True
    )


class CustomConfirmImportForm(ConfirmImportForm):
    exchange = forms.ModelChoiceField(
        queryset=Exchange.objects.all(),
        required=True
    )
