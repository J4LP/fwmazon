from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home/index.html'


class GuidelinesView(TemplateView):
    template_name = 'home/guidelines.html'