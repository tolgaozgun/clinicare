from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.forms import ClearableFileInput
from .models import Product


class AddProductForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    images = forms.ImageField(widget=ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Product
        fields = ['name', 'slug', 'description', 'price']
                  # 'coverImage']

    def clean(self):
        super(AddProductForm, self).clean()

        value_name = self.cleaned_data.get('name')
        value_slug = self.cleaned_data.get('slug')
        value_desc = self.cleaned_data.get('description')
        value_price = self.cleaned_data.get('price')
        value_image = self.cleaned_data.get('images')

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Product name',
            'slug': 'Product url',
            'description': 'Product description',
            'price': 'Price',
            # 'coverImage': 'Cover Image',
            'images': 'Product Images',
        }
        for key, value in placeholders.items():
            self.fields[key].widget.attrs['placeholder'] = value
            self.fields[key].widget.attrs['class'] = 'form-control'


class EditProductForm(forms.ModelForm):
    images = forms.ImageField(widget=ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Product
        fields = ['name', 'slug', 'description', 'price']

    def clean(self):
        super(EditProductForm, self).clean()

        value_name = self.cleaned_data.get('name')
        value_slug = self.cleaned_data.get('slug')
        value_desc = self.cleaned_data.get('description')
        value_price = self.cleaned_data.get('price')
        value_image = self.cleaned_data.get('images')

