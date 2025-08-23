from django import forms

from .models import Product, Review

REVIEW_CHOICES = [
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
]

class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'
        self.fields['is_available'].widget.attrs.update(
            {'class': 'form-check-input'})

    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price',
                  'image', 'alt_text', 'is_available']


class ReviewForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Review
        fields = ['subject', 'content', 'rating']

        # widgets = {
        #     "rating": forms.RadioSelect(choices=REVIEW_CHOICES),
        #     "content": forms.Textarea(attrs={"class": "form-control shadow px-2", "rows": 6}),
        # }
