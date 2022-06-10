from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        validation_errors = response.data.copy()
        response.data.clear()

        response.data["errors"] = validation_errors

    return response


