import gevent
import pandas as pd

from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator
from django.conf import settings

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import Instruments
from .manager import get_factor_index_to_ticker


class InstrumentsView(APIView):

    def get(self, request, version):
        pass

