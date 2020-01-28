import gevent
import pandas as pd
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator
from django.conf import settings

from  .models import Instruments


class InstrumentsView(APIView):

    def get(self, request, version):
        xx = "三"
        params = {
            "iuid": "CN_689801",
            "name": xx,
            "board": "SH",
            "base_volatility": 25.5,
            "base_volume": 55555555.55,
            "status": 1
        }
        _ = Instruments.objects.create(**params)
        return Response({})

