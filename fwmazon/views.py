from django.views.generic import TemplateView


class FwmazonTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = self.get_request_context_data(request, **kwargs)
        return self.render_to_response(context)

    def get_request_context_data(self, request, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        return kwargs