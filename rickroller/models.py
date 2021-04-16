import secrets

from django.db import models
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


class RickrollPost(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("Title"))
    description = models.TextField(max_length=150, verbose_name=_("Description"))
    slug = models.CharField(max_length=50, verbose_name=_("Slug"), unique_for_date=True)
    image = models.URLField(
        verbose_name=_("Image URL"),
        help_text=_("You can provide an image for extra trickery."),
        blank=True,
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))
    redirect_url = models.URLField(
        max_length=512,
        blank=True,
        null=True,
        verbose_name=_("Redirect URL"),
        help_text=_(
            'Redirect URL. Defaults to Rick Astley\'s "Never Gonna Give You Up" offical VEVO video on YouTube.'
        ),
    )

    class Meta:
        verbose_name = _("Rickroll Post")
        verbose_name_plural = _("Rickroll Posts")
        indexes = [
            models.Index(fields=["date", "slug"]),
        ]

    def get_absolute_url(self):
        return reverse_lazy(
            "rickroll:show",
            kwargs={
                "year": self.date.year,
                "month": self.date.month,
                "day": self.date.day,
                "slug": self.slug,
            },
        )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)[:45] + "-" + secrets.token_hex(2)
        return super(RickrollPost, self).save(*args, **kwargs)
