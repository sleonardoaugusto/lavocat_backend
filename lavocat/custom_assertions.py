from unittest import TestCase


class CustomAssertions(TestCase):
    def assertValidationErrorCode(self, serializer, field, code):
        serializer.is_valid()

        errors = serializer.errors
        errors_list = errors[field]
        exception = errors_list[0]

        self.assertEqual(exception.code, code)


_custom_assertions = CustomAssertions()

assert_validation_error_code = _custom_assertions.assertValidationErrorCode
