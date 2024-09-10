from typing import Any
from django import forms
from orders.models import Order
import re


class OrderForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    requires_delivery = forms.ChoiceField(
        choices=[
            ('0', False),
            ('1', True),
        ]
    )
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(choices=[
        ('0', False),
        ('1', True),
    ])

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']

        if not data.isdigit():
            raise forms.ValidationError('Number should consist only digits')
        
        pattern = re.compile(r'^\d{10}$')
        if not pattern.match(data):
            raise forms.ValidationError('Not correct format')
        return data

    # first_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Enter your name'
    #         }
    #     )
    # )
    # last_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Enter your surname'
    #         }
    #     )
    # )
    # phone_number = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Enter your phone number'
    #         }
    #     )
    # )

    # requires_delivery = forms.ChoiceField(
    #     widget=forms.RadioSelect(
    #         choices= [
    #             ('0', False),
    #             ('1', True)
    #         ],
    #        initial = 0,
    #     )
    # )

    # delivery_address = forms.CharField(
    #     widget=forms.Textarea(
    #         attrs={
    #             'class': 'form-control',
    #             'id': 'delivery address',
    #             'rows': 2,
    #             'placeholder': 'Enter your address of delivery'
    #         }
    #     )
    # )

    # payment_on_get = forms.ChoiceField(
    #     widget=forms.RadioSelect(
    #         choices=[
    #             ('0', False),
    #             ('1', True)
    #         ],
    #         initial = 'card'
    #     )
    # )