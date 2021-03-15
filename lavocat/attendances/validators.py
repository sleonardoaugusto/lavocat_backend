from django.core.exceptions import ValidationError


def validate_document_id(value):
    if not len(str(value)) == 11:
        raise ValidationError('Field value must have 11 length', 'length')
