import binascii

from django.core.exceptions import ValidationError
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _


class HexValidator:
    """This HEX-validator from django-extension library.
    https://github.com/django-extensions/django-extensions/
    """
    messages = {
        'invalid': _("Only a hex string is allowed."),
        'length': _("Invalid length. Must be %(length)d characters."),
        'min_length': _("Ensure that there are more than %(min)s characters."),
        'max_length': _(
            "Ensure that there are no more than %(max)s characters."),
    }
    code = "hex_only"

    def __init__(self, length=None, min_length=None, max_length=None,
                 message=None, code=None):
        self.length = length
        self.min_length = min_length
        self.max_length = max_length
        if message:
            self.message = message
        else:
            self.message = self.messages['invalid']
        if code:
            self.code = code

    def __call__(self, value):
        value = force_str(value)
        if self.length and len(value) != self.length:
            raise ValidationError(self.messages['length'],
                                  code='hex_only_length',
                                  params={'length': self.length})
        if self.min_length and len(value) < self.min_length:
            raise ValidationError(self.messages['min_length'],
                                  code='hex_only_min_length',
                                  params={'min': self.min_length})
        if self.max_length and len(value) > self.max_length:
            raise ValidationError(self.messages['max_length'],
                                  code='hex_only_max_length',
                                  params={'max': self.max_length})

        try:
            binascii.unhexlify(value[1:])
        except (TypeError, binascii.Error):
            raise ValidationError(self.messages['invalid'], code='hex_only')

    def __eq__(self, other):
        return (
                isinstance(other, HexValidator) and
                (self.message == other.message) and
                (self.code == other.code)
        )
