from django.urls import path
from .medical import urlpatterns as medical_urls
from .user import urlpatterns as user_urls
from .material import urlpatterns as material_urls
from .project import urlpatterns as project_urls
from .statistics import urlpatterns as statistics_urls
from .activity import urlpatterns as activity_urls
from .news import urlpatterns as news_urls
from .list_all_requests import urlpatterns as list_all_requests_urls


urlpatterns =  medical_urls + user_urls + material_urls + project_urls + statistics_urls + activity_urls + news_urls + list_all_requests_urls

