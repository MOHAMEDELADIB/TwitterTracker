from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView







class ChangeLanguageView(TemplateView):
    template_name = 'main/change_language.html'
