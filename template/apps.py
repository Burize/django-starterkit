import os

from django.apps import AppConfig


class TemplateConfig(AppConfig):
    name = 'template'

    def ready(self):
        self._notify_nginx_application_ready()

    def _notify_nginx_application_ready(self):
        """
            This starterkit is adapted for use with Heroku+Nginx
            need fot https://elements.heroku.com/buildpacks/heroku/heroku-buildpack-nginx
        """
        if os.path.isdir('/tmp'):
            with open('/tmp/app-initialized', 'w+'):
                pass