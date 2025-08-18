
from cinema.models import SeoBlock, Image
from django import forms
from django.forms import modelformset_factory
from dashboard.models import Page, MainPage, ContactPage, Cinema
from cinema.models import SeoBlock, Image

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ["title", "slug", "content", "image", "is_active"]  # gallery убрали из основной формы
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["image", "alt_text"]
        widgets = {
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "alt_text": forms.TextInput(attrs={"class": "form-control", "placeholder": "alt"}),
        }

ImageFormSet = modelformset_factory(
    Image,
    form=ImageForm,
    extra=4,          # как в макете — свободные слоты "Добавить"
    can_delete=True,
)

class SeoBlockForm(forms.ModelForm):
    class Meta:
        model = SeoBlock
        fields = ["slug", "title", "keywords", "description"]
        widgets = {
            "slug": forms.TextInput(attrs={"class": "form-control form-control-sm", "placeholder": "URL"}),
            "title": forms.TextInput(attrs={"class": "form-control form-control-sm", "placeholder": "Title"}),
            "keywords": forms.TextInput(attrs={"class": "form-control form-control-sm", "placeholder": "Keywords"}),
            "description": forms.Textarea(attrs={"class": "form-control form-control-sm", "rows": 3, "placeholder": "Description"}),
        }

class MainPageForm(forms.ModelForm):
    class Meta:
        model = MainPage
        fields = ["phone_1", "phone_2", "seo_text", "is_active"]


class ContactPageForm(forms.ModelForm):
    """Редактируем только флаг активности. Язык проставим во view."""
    class Meta:
        model = ContactPage
        fields = ["is_active"]
        widgets = {
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class CinemaForm(forms.ModelForm):
    """Все обязательные поля из модели Cinema вынесены в форму."""
    class Meta:
        model = Cinema
        fields = [
            "name",
            "slug",
            "city",
            "address",
            "phone_number",
            "description",
            "map_coordinates",
            "image",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Название кинотеатра"}),
            "slug": forms.TextInput(attrs={"class": "form-control", "placeholder": "slug (необязательно)"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "Город"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Адрес"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "+380XXXXXXXXX"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Описание"}),
            "map_coordinates": forms.TextInput(attrs={"class": "form-control", "placeholder": "50.4501, 30.5234"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }









# class SeoForm(forms.Form):
#     seo_url = forms.CharField(
#         label="URL", widget=forms.TextInput(attrs={"class": "form-control"})
#     )
#     seo_title = forms.CharField(
#         label="Title", widget=forms.TextInput(attrs={"class": "form-control"})
#     )
#     seo_keywords = forms.CharField(
#         label="Keywords", widget=forms.TextInput(attrs={"class": "form-control"})
#     )
#     seo_description = forms.CharField(
#         label="Description", widget=forms.Textarea(attrs={"class": "form-control"})
#     )


# class CinemaForm(forms.Form):
#     name = forms.CharField(
#         label="Название кинотеатра",
#         widget=forms.TextInput(attrs={"class": "form-control"}),
#     )
#     description = forms.CharField(
#         label="Описание", widget=forms.Textarea(attrs={"class": "form-control"})
#     )
#     conditions = forms.CharField(
#         label="Условия",
#         widget=forms.Textarea(attrs={"class": "form-control"}),
#         required=False,
#     )


# class HallForm(forms.Form):
#     number = forms.CharField(
#         label="Номер зала", widget=forms.TextInput(attrs={"class": "form-control"})
#     )
#     description = forms.CharField(
#         label="Описание зала", widget=forms.Textarea(attrs={"class": "form-control"})
#     )


# class NewsForm(forms.Form):
#     title = forms.CharField(
#         label="Название новости",
#         widget=forms.TextInput(
#             attrs={"class": "form-control", "placeholder": "Название новости"}
#         ),
#     )
#     description = forms.CharField(
#         label="Описание",
#         widget=forms.Textarea(
#             attrs={"class": "form-control", "rows": 5, "placeholder": "Описание"}
#         ),
#     )
#     date_published = forms.DateField(
#         label="Дата публикации",
#         widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
#     )
#     status = forms.BooleanField(label="ВКЛ", required=False)

#     video_url = forms.URLField(
#         label="Ссылка на видео",
#         required=False,
#         widget=forms.URLInput(
#             attrs={"class": "form-control", "placeholder": "Ссылка на видео в youtube"}
#         ),
#     )
