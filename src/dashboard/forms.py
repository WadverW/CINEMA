from django import forms


class SeoForm(forms.Form):
    seo_url = forms.CharField(
        label="URL", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    seo_title = forms.CharField(
        label="Title", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    seo_keywords = forms.CharField(
        label="Keywords", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    seo_description = forms.CharField(
        label="Description", widget=forms.Textarea(attrs={"class": "form-control"})
    )


class CinemaForm(forms.Form):
    name = forms.CharField(
        label="Название кинотеатра",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    description = forms.CharField(
        label="Описание", widget=forms.Textarea(attrs={"class": "form-control"})
    )
    conditions = forms.CharField(
        label="Условия",
        widget=forms.Textarea(attrs={"class": "form-control"}),
        required=False,
    )


class HallForm(forms.Form):
    number = forms.CharField(
        label="Номер зала", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    description = forms.CharField(
        label="Описание зала", widget=forms.Textarea(attrs={"class": "form-control"})
    )


class NewsForm(forms.Form):
    title = forms.CharField(
        label="Название новости",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Название новости"}
        ),
    )
    description = forms.CharField(
        label="Описание",
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": 5, "placeholder": "Описание"}
        ),
    )
    date_published = forms.DateField(
        label="Дата публикации",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    status = forms.BooleanField(label="ВКЛ", required=False)

    video_url = forms.URLField(
        label="Ссылка на видео",
        required=False,
        widget=forms.URLInput(
            attrs={"class": "form-control", "placeholder": "Ссылка на видео в youtube"}
        ),
    )
