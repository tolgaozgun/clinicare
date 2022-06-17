from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from .models import BlogPost, BlogCategory


class BlogPostForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = BlogPost
        fields = ['title', 'slug', 'description', 'text', 'image']

    def clean(self):
        super().clean()

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'title': 'Enter a post title',
            'slug': 'Enter post URL',
            'description': 'Enter post description',
            'text': 'Enter the post content',
            'image': 'Enter cover image',
        }
        for key, value in placeholders.items():
            self.fields[key].widget.attrs['placeholder'] = value
            self.fields[key].widget.attrs['class'] = 'form-control'


class BlogCategoryForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = BlogCategory
        fields = ['name', 'slug', 'description', 'image']

    def clean(self):
        super().clean()

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'title': 'Enter a post title',
            'slug': 'Enter post URL',
            'description': 'Enter post description',
            'image': 'Enter cover image',
        }
        for key, value in placeholders.items():
            self.fields[key].widget.attrs['placeholder'] = value
            self.fields[key].widget.attrs['class'] = 'form-control'

