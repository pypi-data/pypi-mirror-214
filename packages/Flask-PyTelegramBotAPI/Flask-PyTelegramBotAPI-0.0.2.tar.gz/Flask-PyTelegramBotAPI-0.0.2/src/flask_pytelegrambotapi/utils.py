from werkzeug.local import LocalProxy

from flask import (_request_ctx_stack, current_app, request, session, url_for, g,
                   has_request_context)

current_user = LocalProxy(lambda: _get_user())


def _get_user():
    if has_request_context() and not hasattr(_request_ctx_stack.top, 'user'):
        # current_app.login_manager._load_user()
        current_app.pytelegrambotapi.get_user()

    return getattr(_request_ctx_stack.top, 'user', None)
