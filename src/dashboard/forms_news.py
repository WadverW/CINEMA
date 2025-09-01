from django import forms
from django.forms import modelformset_factory
from cinema.models import Image, SeoBlock
from promotion.models import PromoNews


class NewsForm(forms.ModelForm):
    class Meta:
        model = PromoNews
        fields = [
            "title",
            "published_at",
            "text",
            "image",
            "link_on_video",
            "is_active",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "published_at": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "link_on_video": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ссылка на видео (YouTube, Vimeo и т.п.)",
                    "inputmode": "url",
                }
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    # необязательно: если хочешь принимать только https-ссылки
    def clean_link_on_video(self):
        url = self.cleaned_data.get("link_on_video")
        if url and not url.startswith(("http://", "https://")):
            url = "https://" + url
        return url


class SeoBlockForm(forms.ModelForm):
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


class ImageForm(forms.ModelForm):
    alt_text = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "alt"}),
    )

    class Meta:
        model = Image
        fields = ["image", "alt_text"]
        widgets = {"image": forms.ClearableFileInput(attrs={"class": "form-control"})}


ImageFormSet = modelformset_factory(Image, form=ImageForm, can_delete=True, extra=5)
