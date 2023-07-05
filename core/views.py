from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .models import Encuentro


class Dashboard(View):
    def get(self, request):
        ctx = {'quarterfinals': Encuentro.objects.filter(
            ronda__fase__nombre='Fase Eliminatoria')}
        return render(request, template_name='dashboard.html', context=ctx)
