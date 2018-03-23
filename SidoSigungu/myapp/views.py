from django.shortcuts import render
from django.views.generic.base import TemplateView
import json
from django.http.response import HttpResponse
from django.db import connection


# Create your views here.
class IndexPageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)
    
    def getSido(self, *args, **kwargs):
        cursor = connection.cursor()
        cursor.execute("select code as code,sido as sido from districtcode group by sido order by id asc")
        rows = cursor.fetchall()
        data = []
        item = {}
        for result in rows:
            item = {'code': result[0], 'sido': result[1]}
            data.append(item)
            item = {}

        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type="application/json")
    
    def getSigungu(request, *args, **kwargs):
        print("getSigungu---------------------------"+request.GET["sido"])
        cursor = connection.cursor()
        sido = request.GET.get('sido', None)
        cursor.execute("select code,gugun from districtcode where sido=(select sido from districtcode  WHERE code = %s )order by id asc", [sido] )
        rows = cursor.fetchall()
        data = []
        item = {}
        for result in rows:
            item = {'code': result[0], 'sido': result[1]}
            data.append(item)
            item = {}

        json_data = json.dumps(data)
        return HttpResponse(json_data, content_type="application/json")