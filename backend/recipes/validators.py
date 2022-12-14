import binascii

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _


@deconstructible
class HexValidator:
    """HEX-validator for check color in Tag model."""
    messages = {
        'invalid': _("Only a hex string is allowed."),
        'length': _("Invalid length. Must be %(length)d characters."),
    }
    code = "hex_only"

    def __init__(self, length=None, code=None):
        self.length = length
        self.message = self.messages['invalid']
        if code:
            self.code = code

    def __call__(self, value):
        value = force_str(value)
        if self.length and len(value) != self.length:
            raise ValidationError(self.messages['length'],
                                  code='hex_only_length',
                                  params={'length': self.length})
        try:
            binascii.unhexlify(value[1:])
        except (TypeError, binascii.Error):
            raise ValidationError(self.messages['invalid'], code='hex_only')
