from django.shortcuts import render
from django.views.generic import View
from django.conf import settings
import os

class FrontendAppView(View):
    def get(self, request):
        try:
            with open(os.path.join(settings.BASE_DIR, '..', 'frontend', 'build', 'index.html')) as f:
                return render(request, 'index.html', {})
        except FileNotFoundError:
            # Handle the case where index.html is not found,
            # possibly by rendering a different template or returning a 404 error.
            # For now, let's assume it's always there in a production setup.
            # In development, ensure the React app is built.
            return render(request, 'index.html', {}) # This will likely fail if the file truly doesn't exist
                                                    # but Django will show a TemplateDoesNotExist error.
                                                    # A more robust solution is needed for production.
