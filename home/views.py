from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from client.models import Plan

class HomeView(TemplateView):

    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None

        plans = Plan.objects.all()
        return render(request, 'home/home.html', {'user': user, 'plans': plans})