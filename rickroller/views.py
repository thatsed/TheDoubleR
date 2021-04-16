import re

from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_control, cache_page
from django.views.decorators.vary import vary_on_headers
from django.views.generic import CreateView, ListView, TemplateView

from rickroller.forms import RickrollPostForm
from rickroller.models import RickrollPost


@method_decorator(vary_on_headers("Accept-Language"), name="dispatch")
@method_decorator(cache_control(public=True), name="dispatch")
@method_decorator(cache_page(60 * 60), name="dispatch")
class AboutView(TemplateView):
    template_name = "rickroller/about.html"


@method_decorator(vary_on_headers("Accept-Language"), name="dispatch")
@method_decorator(cache_control(public=True), name="dispatch")
@method_decorator(cache_page(60 * 60), name="dispatch")
class RickrollPostCreateView(CreateView):
    model = RickrollPost
    form_class = RickrollPostForm

    def get_success_url(self):
        return reverse(
            "rickroll:show",
            kwargs={
                "year": self.object.date.year,
                "month": self.object.date.month,
                "day": self.object.date.day,
                "slug": self.object.slug,
            },
        ).replace("/posts/", "/share/#/")


@method_decorator(vary_on_headers("Accept-Language"), name="dispatch")
@method_decorator(cache_control(public=True), name="dispatch")
@method_decorator(cache_page(60 * 60), name="dispatch")
class RickrollPostShareView(TemplateView):
    template_name = "rickroller/share.html"


@method_decorator(vary_on_headers("Accept-Language"), name="dispatch")
@method_decorator(cache_control(public=True, max_age=10), name="dispatch")
@method_decorator(cache_page(10), name="dispatch")
class RickrollPostListView(ListView):
    # disabled due to privacy concerns
    model = RickrollPost
    context_object_name = "posts"
    paginate_by = 6


class RickrollPostShowView(View):
    redirect_url = settings.RICKROLL_URL
    bot_user_agents = [
        re.compile(r".*TwitterBot.*"),
        re.compile(r".*TelegramBot.*"),
        re.compile(r".*Twitterbot.*"),
        re.compile(r".*bingbot.*"),
        re.compile(r".*WhatsApp.*"),
        re.compile(r".*Discordbot.*"),
        re.compile(r".*redditbot.*"),
    ]

    @method_decorator(vary_on_headers("User-Agent"))
    @method_decorator(cache_control(public=True))
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        for bot in self.bot_user_agents:
            if bot.match(user_agent):
                return self.bots(request, *args, **kwargs)
        return self.redirect(request, *args, **kwargs)

    def redirect(self, request, year, month, day, slug):
        """
        User requests handler.

        Redirects the user to the ``redirect_url`` of the post if it exists, else to the default ``RICKROLL_URL``
        specified in settings.
        """
        try:
            post = RickrollPost.objects.get(
                date__year=year, date__month=month, date__day=day, slug=slug
            )
        except RickrollPost.DoesNotExist:
            return redirect(settings.RICKROLL_URL, permanent=True)
        return redirect(post.redirect_url or settings.RICKROLL_URL, permanent=True)

    @method_decorator(cache_page(60 * 60))
    def bots(self, request, year, month, day, slug):
        """
        Bot requests handler.

        Returns a rendered HTML page with fake article meta tags.
        """
        post = get_object_or_404(
            RickrollPost, date__year=year, date__month=month, date__day=day, slug=slug
        )
        return render(request, "rickroller/bots.html", {"post": post})
