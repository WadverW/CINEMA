from django import forms
from django.forms import modelformset_factory
from cinema.models import Cinema, Hall, Image, SeoBlock

class CinemaCardForm(forms.ModelForm):
    class Meta:
        model = Cinema
        fields = [
            "name", "description", "address", "city",
            "phone_number", "map_coordinates", "image"
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "map_coordinates": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}), 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["address"].required = False
        self.fields["city"].required = False
        self.fields["phone_number"].required = False
        self.fields["map_coordinates"].required = False

class ImageForm(forms.ModelForm):
    alt_text = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "alt"})
    )

    class Meta:
        model = Image
        fields = ["image", "alt_text"]
        widgets = {
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

ImageFormSet = modelformset_factory(
    Image,
    form=ImageForm,
    can_delete=True,
    extra=5,  
)




class HallForm(forms.ModelForm):
    """Основные поля зала (как на макете)."""
    class Meta:
        model = Hall
        fields = ["name", "description", "rows", "is_vip", "map_hall"]
        labels = {
            "name": "Номер зала",
            "description": "Описание зала",
            "rows": "Количество рядов",
            "is_vip": "VIP зал",
            "map_hall": "Схема зала",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например: 8 зал"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 6, "placeholder": "текст"}),
            "rows": forms.NumberInput(attrs={"class": "form-control"}),
            "is_vip": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "map_hall": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class SeoBlockForm(forms.ModelForm):
    """SEO блок внизу формы."""
    class Meta:
        model = SeoBlock
        fields = ["slug", "title", "keywords", "description"]
        labels = {
            "slug": "URL",
            "title": "Title",
            "keywords": "Keywords",
            "description": "Description",
        }
        widgets = {
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "keywords": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }


class HallImageForm(forms.ModelForm):

    alt_text = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "alt"})
    )

    class Meta:
        model = Image
        fields = ["image", "alt_text"]
        widgets = {
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


HallGalleryFormSet = modelformset_factory(
    Image,
    form=HallImageForm,
    can_delete=True,
    extra=5,         
)