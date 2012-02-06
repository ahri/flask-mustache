# coding: utf-8

def viewroute(app, rule):
    """Decorator for a pystache View"""

    def class_wrapper(c):

        def render(**kwargs):
            o = c()
            o.route_args = kwargs
            return o.render()

        app.add_url_rule(rule, c.__name__, render)

        return c

    return class_wrapper

def viewerror(app, code_or_exception, return_code=None):
    """Decorator for a pystache error View"""

    if return_code is None:
        if type(code_or_exception) is int:
            return_code = code_or_exception
        else:
            return_code = 500

    def class_wrapper(c):

        def render(err, **kwargs):
            o = c()
            o.err = err
            o.route_args = kwargs
            return o.render(), return_code

        app.register_error_handler(code_or_exception, render)

        return c

    return class_wrapper
