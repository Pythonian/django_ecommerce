from django import forms

from .models import Product, Review


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
                  'image', 'alt_text', 'is_available', 'units']


class ReviewForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Review
        fields = ['subject', 'content', 'rating']


# class ReviewForm(forms.ModelForm):

#     class Meta:
#         model = Review
#         fields = ['text', 'rating']

#         widgets = {
#             'text': forms.Textarea(
#                 attrs={
#                     'class': 'form-control shadow px-2',
#                     'rows': 6
#                 }
#             ),
#             'rating': forms.RadioSelect
#         }
