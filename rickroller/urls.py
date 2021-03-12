from django.urls import path

from rickroller import views

app_name = 'rickroller'

urlpatterns = [
    path('', views.RickrollPostCreateView.as_view(), name='create'),
    path('about', views.AboutView.as_view(), name='about'),
    path('share/', views.RickrollPostShareView.as_view(), name='share'),
    path('posts/<int:year>/<int:month>/<int:day>/<slug:slug>', views.RickrollPostShowView.as_view(), name='show'),
    # path('posts/list', views.RickrollPostListView.as_view(), name='list'),  # disabled due to privacy concerns
]
