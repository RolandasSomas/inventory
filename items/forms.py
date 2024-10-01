from django import forms
from .models import Item, ItemType, Location, ItemCategory


# ItemsForm
class ItemForm(forms.Form):
    name = forms.ModelChoiceField(
        queryset=ItemType.objects.all(),
        required=False,
        empty_label="Select an option"
    )
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        required=False,
        empty_label="Select an option"
    )


class LocationForm(forms.Form):
    name = forms.CharField(
        max_length=10,
        required=False)
    location = forms.CharField(
        max_length=10,
        required=False)


class CategoryForm(forms.Form):
    title = forms.CharField(
        max_length=10,
        required=False)


class ItemsForm(forms.Form):
    serial_number = forms.CharField(
        max_length=10,
        required=False)
    title = forms.CharField(
        max_length=10,
        required=False)
    category = forms.ModelChoiceField(
        queryset=ItemCategory.objects.all(),
        required=False,
        empty_label="Select an option"
    )

