import gevent
import pandas as pd

from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator
from django.conf import settings

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import Instruments
from .manager import iuid_to_df


class InstrumentsView(APIView):

    def get(self, request, version):
        Instruments.objects.filter(name__startswith="*ST").update(status=0)
        Instruments.objects.filter(size_in_file__lt=150).update(status=0)
        a = iuid_to_df("002665")
        return Response({})

