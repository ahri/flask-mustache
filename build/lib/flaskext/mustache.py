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
