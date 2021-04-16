from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from rickroller.models import RickrollPost


class RickrollPostForm(forms.ModelForm):
    class Meta:
        model = RickrollPost
        fields = ('title', 'description', 'image', 'redirect_url')
        widgets = {
            'title': forms.Textarea(attrs={
                'data-nonl': True,
                'class': "form-control bg-dark preview-title text-white border-0 mb-1",
                "placeholder": _("Title"),
                "autocomplete": "off",
                "rows": 1,
            }),
            'description': forms.Textarea(attrs={
                'class': "form-control bg-dark preview-description text-white border-0 mb-1",
                "placeholder": _("Description"),
                "autocomplete": "off",
                "rows": 4,
            }),
            'image': forms.URLInput(attrs={
                'class': "form-control bg-dark border-0 text-light",
                "placeholder": _("Image URL"),
                "autocomplete": "off",
            }),
            'redirect_url': forms.URLInput(attrs={
                'class': "form-control bg-dark border-0 text-light",
                "placeholder": settings.RICKROLL_URL,
                "autocomplete": "off",
            }),
        }
