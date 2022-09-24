from django.shortcuts import render

from django.views import View
from django.http import JsonResponse
from bet.models import BetOdds


# Create your views here.

class BetOddView(View):

    def get(self, request):
        pass

    def post(self, request):
        pass
