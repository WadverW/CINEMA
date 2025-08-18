from django import forms
from django.forms.widgets import ClearableFileInput
from cinema.models import Movie, Image, SeoBlock

class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True

class MovieForm(forms.ModelForm):

    new_gallery = forms.FileField(
        required=False,
        widget=MultipleFileInput(attrs={"multiple": True, "class": "form-control"}),
        label="Добавить в галерею",
    )

    class Meta:
        model = Movie
        fields = [
            "title", "slug", "description", "poster",
            "trailer_url", "age_rating", "release_date", "is_coming_soon",
            "is_2d", "is_3d", "is_imax",
        ]
        widgets = {
            "title":        forms.TextInput(attrs={"class": "form-control", "placeholder": "Название фильма"}),
            "slug":         forms.TextInput(attrs={"class": "form-control", "placeholder": "slug"}),
            "description":  forms.Textarea(attrs={"class": "form-control", "placeholder": "Описание фильма", "rows": 5}),
            "poster":       ClearableFileInput(attrs={"class": "form-control"}),
            "trailer_url":  forms.URLInput(attrs={"class": "form-control", "placeholder": "Ссылка на трейлер"}),
            "age_rating":   forms.TextInput(attrs={"class": "form-control", "placeholder": "Возрастной рейтинг"}),
            "release_date": forms.DateInput(attrs={"type": "date", "class": "form-control", "placeholder": "Дата выхода"}),
            "is_coming_soon": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_2d":        forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_3d":        forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_imax":      forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

class ImageForm(forms.ModelForm):
    alt_text = forms.CharField(required=False)
    class Meta:
        model = Image
        fields = ["image", "alt_text"]
        widgets = {
            "image":    ClearableFileInput(attrs={"class": "form-control"}),
            "alt_text": forms.TextInput(attrs={"class": "form-control", "placeholder": "alt"}),
        }

from django.forms import modelformset_factory
ImageFormSet = modelformset_factory(
    Image,
    form=ImageForm,
    can_delete=True,
    extra=4,
)

class SeoBlockForm(forms.ModelForm):
    class Meta:
        model = SeoBlock
        fields = ["slug", "title", "keywords", "description"]
        widgets = {
            "slug":        forms.TextInput(attrs={"class": "form-control", "placeholder": "URL"}),
            "title":       forms.TextInput(attrs={"class": "form-control", "placeholder": "Title"}),
            "keywords":    forms.TextInput(attrs={"class": "form-control", "placeholder": "word"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Description"}),
        }
