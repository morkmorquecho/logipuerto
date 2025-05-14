from datetime import datetime
import os
from django.contrib import messages

#esta clase mixin permite manejar los messages de django, util para no repetirar el mismo codigo en cada vista adaptado igual para ser utilizado en sweetAlerts
class MessageMixin:
    def add_message(self, level, message, extra_tags='', fail_silently=False):
        messages.add_message(
            self.request,
            level,
            message,
            extra_tags=extra_tags,
            fail_silently=fail_silently
        )

    def success(self, message, **kwargs):
        self.add_message(messages.SUCCESS, message, **kwargs)

    def error(self, message, **kwargs):
        self.add_message(messages.ERROR, message, **kwargs)

    def info(self, message, **kwargs):
        self.add_message(messages.INFO, message, **kwargs)

    def warning(self, message, **kwargs):
        self.add_message(messages.WARNING, message, **kwargs)


