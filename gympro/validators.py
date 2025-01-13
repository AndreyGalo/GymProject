from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re

#https://docs.djangoproject.com/en/5.1/topics/auth/passwords/#django.contrib.auth.password_validation.validate_password
class CustomPasswordValidator:
    """
    https://awstip.com/create-your-own-custom-password-validator-in-django-6bc75ddcf126
    https://docs.djangoproject.com/en/5.1/topics/auth/passwords/#django.contrib.auth.password_validation.validate_password
    """
    def validate(self, password, user=None):
        if not re.search(r'\d', password):
            raise ValidationError(
                "This password must contain at least one digit",
                code='password_no_number',
            )

    def get_help_text(self):
        return "This password must contain at least one digit"