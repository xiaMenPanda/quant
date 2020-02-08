import gevent
import pandas as pd

from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator
from django.conf import settings

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import Instruments



class InstrumentsView(APIView):

    def get(self, request, version):
        pass

