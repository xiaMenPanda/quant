"""trading URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from .views import InstrumentsView

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='User API')

api_pattern = [
    url(r'^instruments$', InstrumentsView.as_view()),
    ]

versions_patterns = [
    url(r'^(?P<version>v\d+)/txd/', include(api_pattern)),
]

urlpatterns = [
    url(r'^docs/txd$', schema_view, name='schema-swagger-ui'),
    url(r'^', include(versions_patterns)),
]
