from django.core.exceptions import ValidationError


def rate_validate(value):
    if not (0 <= value <= 5):
        raise ValidationError('must be between 0-5')





