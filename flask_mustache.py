# coding: utf-8
from pystache import render


class FlaskMustache(object):

    def __init__(self, app, renderer=render):
        self._app = app
        self._renderer = renderer

    def view_route(self, rule):
        """Decorator for a pystache View"""

        def class_wrapper(c):

            def _render(**kwargs):
                o = c()
                try:
                    o.route(**kwargs)
                except AttributeError:
                    pass  # route is optional

                return self._renderer(o)

            self._app.add_url_rule(rule, c.__name__, _render)

            return c

        return class_wrapper

    def view_error(self, code_or_exception, return_code=None):
        """Decorator for a pystache error View"""

        if return_code is None:
            if type(code_or_exception) is int:
                return_code = code_or_exception
            else:
                return_code = 500

        def class_wrapper(c):

            def _render(err, **kwargs):
                o = c()
                o.err = err
                try:
                    o.route(**kwargs)
                except AttributeError:
                    pass  # route is optional

                return self._renderer(o), return_code

            self._app.register_error_handler(code_or_exception, _render)

            return c

        return class_wrapper
