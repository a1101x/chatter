from rest_framework.views import exception_handler


def chatter_exception_handler(exc, context):
    """
    Custom exception handler.
    Merge all fields in errors key.
    """
    response = exception_handler(exc, context)

    if response is not None:
        errors = {}

        for field, value in response.data.items():
            errors[field] = ' '.join(value)

        response.data = {}
        response.data['errors'] = errors
        
    return response
