
from django.contrib import admin
from django.urls import path
from dashboard import views
from scraper.views import run_task, get_status


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path("scrape/<task_id>/", get_status, name="get_status"),
    path("scrape/", run_task, name="run_task"),
    path("dashboard/", views.home, name="home"),
    # path('dashboard/<str:product_name>', views.search, name='search')

]
