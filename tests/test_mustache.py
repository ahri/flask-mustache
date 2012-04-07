# coding: utf-8

from flask import Flask
from flaskext.testing import TestCase
from pystache import View

import sys
sys.path.append("flaskext")
from mustache import viewroute, viewerror

class Decorator(TestCase):

    """
    Test the view decorator.
    """

    def create_app(self):
        """Make a test app"""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        return self.app

    def setup_view(self, *args, **kwargs):
        """Create a view and decorate it with our pystache viewroute"""

        @viewroute(self.app, *args, **kwargs)
        class Example(View):

            """
            An example view
            """

            def __init__(self, *args, **kwargs):
                super(Example, self).__init__(*args, **kwargs)
                self.template = "{{hello}}{{dynamic}}"

            def route(self, **kwargs):
                self.route_args = kwargs

            def hello(self):
                return "hello"

            def dynamic(self):
                return self.route_args.get('dynamic')

    def test_valid_response(self):
        """Test that the application gives a valid response for our test route"""
        # Arrange
        route = '/test'
        self.setup_view(route)

        # Act
        response = self.client.get(route)

        # Assert
        self.assert200(response)

    def test_valid_content_mustache_var(self):
        """Test that the application gives valid content for a template with a simple mustache var to set"""
        # Arrange
        route = '/test'
        self.setup_view(route)

        # Act
        response = self.client.get(route)

        # Assert
        self.assertEquals(response.data, "hello")

    def test_valid_dynamic_content(self):
        """Test that the application gives valid content where a variable is passed on the URL"""
        # Arrange
        route = '/test/<dynamic>'
        self.setup_view(route)

        # Act
        response = self.client.get(route.replace('<dynamic>', 'dynamic'))

        # Assert
        self.assertEquals(response.data, "hellodynamic")

class Decorator404(TestCase):

    """
    Test the view decorator when a 404 occurs.
    """

    def create_app(self):
        """Make a test app"""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        return self.app

    def setup_view(self, *args, **kwargs):
        """Create a view and decorate it with our pystache viewroute"""

        @viewerror(self.app, 404, *args, **kwargs)
        class Example404(View):

            """
            An example 404 view
            """

            def __init__(self, *args, **kwargs):
                super(Example404, self).__init__(*args, **kwargs)
                self.template = "{{hello}}"

            def route(self, **kwargs):
                self.route_args = kwargs

            def hello(self):
                return "hello 404"

    def test_invalid_response(self):
        """Test that the application gives an invalid response for our incorrect test route"""
        # Arrange
        route = '/test404'
        self.setup_view()

        # Act
        response = self.client.get(route)

        # Assert
        self.assert404(response)

    def test_valid_content_mustache_var(self):
        """Test that the application gives valid content for a template with a simple mustache var to set"""
        # Arrange
        route = '/test404'
        self.setup_view()

        # Act
        response = self.client.get(route)

        # Assert
        self.assertEquals(response.data, "hello 404")

class DecoratorException(TestCase):

    """
    Test the view decorator when an exception occurs.
    """

    def create_app(self):
        """Make a test app"""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        return self.app

    def setup_view(self, *args, **kwargs):
        """Create a view and decorate it with our pystache viewroute"""

        @viewroute(self.app, '/testexception', *args, **kwargs)
        class ExampleRaiseException(View):

            """
            An example view
            """

            def __init__(self, *args, **kwargs):
                super(ExampleRaiseException, self).__init__(*args, **kwargs)
                self.template = "{{hello}}"

            def hello(self):
                raise Exception("testing")

        @viewerror(self.app, Exception, *args, **kwargs)
        class ExampleException(View):

            """
            An example Exception view
            """

            def __init__(self, *args, **kwargs):
                super(ExampleException, self).__init__(*args, **kwargs)
                self.template = "{{hello}}{{dynamic}}"

            def route(self, **kwargs):
                self.route_args = kwargs

            def hello(self):
                return "hello exception"

            def dynamic(self):
                return self.route_args.get('dynamic')

    def test_invalid_response(self):
        """Test that the application gives a 500 response when an exception is raised"""
        # Arrange
        route = '/testexception'
        self.setup_view()

        # Act
        response = self.client.get(route)

        # Assert
        self.assertStatus(response, 500)

    def test_valid_content_mustache_var(self):
        """Test that the application renders a template when an exception is raised"""
        # Arrange
        route = '/testexception'
        self.setup_view()

        # Act
        response = self.client.get(route)

        # Assert
        self.assertEquals(response.data, "hello exception")

class DecoratorExCustomCode(TestCase):

    """
    Test the view decorator when an exception occurs and return a custom code.
    """

    def create_app(self):
        """Make a test app"""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        return self.app

    def setup_view(self, *args, **kwargs):
        """Create a view and decorate it with our pystache viewroute"""

        @viewroute(self.app, '/testnotimplemented', *args, **kwargs)
        class ExampleRaiseNotImplemented(View):

            """
            An example view
            """

            def __init__(self, *args, **kwargs):
                super(ExampleRaiseNotImplemented, self).__init__(*args, **kwargs)
                self.template = "{{hello}}{{dynamic}}"

            def route(self, **kwargs):
                self.route_args = kwargs

            def hello(self):
                raise NotImplementedError("testing")

            def dynamic(self):
                return self.route_args.get('dynamic')

        @viewerror(self.app, NotImplementedError, 501, *args, **kwargs)
        class ExampleCustomCode(View):

            """
            An example Exception view
            """

            def __init__(self, *args, **kwargs):
                super(ExampleCustomCode, self).__init__(*args, **kwargs)
                self.template = "{{hello}}"

            def route(self, **kwargs):
                self.route_args = kwargs

            def hello(self):
                return "hello custom code"

    def test_invalid_response(self):
        """Test that the application gives a 501 response when an exception is raised"""
        # Arrange
        route = '/testnotimplemented'
        self.setup_view()

        # Act
        response = self.client.get(route)

        # Assert
        self.assertStatus(response, 501)

    def test_valid_content_mustache_var(self):
        """Test that the application renders a template when an exception is raised"""
        # Arrange
        route = '/testnotimplemented'
        self.setup_view()

        # Act
        response = self.client.get(route)

        # Assert
        self.assertEquals(response.data, "hello custom code")
