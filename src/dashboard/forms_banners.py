from django import forms
from .models import MainUpperBanner, NewsPromoBanner, BgBanner


class UpperBannerForm(forms.ModelForm):
    image_file = forms.ImageField(
        required=False,
        label="Добавить изображение",
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = MainUpperBanner
        fields = ["link", "text", "position", "rotation_speed", "is_active"]
        widgets = {
            "link": forms.URLInput(attrs={"class": "form-control", "placeholder": "URL"}),
            "text": forms.TextInput(attrs={"class": "form-control", "placeholder": "Текст"}),
            "position": forms.NumberInput(attrs={"class": "form-control"}),
            "rotation_speed": forms.NumberInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class NewsBannerForm(forms.ModelForm):
    image_file = forms.ImageField(
        required=False,
        label="Добавить изображение",
    )

    class Meta:
        model = NewsPromoBanner
        fields = ["link", "text", "position", "rotation_speed", "is_active"]
        widgets = {
            "image_file": forms.FileInput(attrs={"class": "form-control", }),
            "link": forms.URLInput(attrs={"class": "form-control", "placeholder": "URL"}),
            "text": forms.TextInput(attrs={"class": "form-control", "placeholder": "Текст"}),
            "position": forms.NumberInput(attrs={"class": "form-control"}),
            "rotation_speed": forms.NumberInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class BgBannerForm(forms.ModelForm):
    BACKGROUND_CHOICES = [
        ("image", "Фото на фоне"),
        ("colore_bg", "Просто фон"),
    ]

    background_type = forms.ChoiceField(
        choices=BACKGROUND_CHOICES,
        widget=forms.RadioSelect,
        label="Тип фона",
    )

    class Meta:
        model = BgBanner
        fields = ["image", "is_active"]
        widgets = {
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

