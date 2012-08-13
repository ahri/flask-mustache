# coding: utf-8

from flask import Flask
from flask.ext.testing import TestCase
from flask.ext.mustache import FlaskMustache

from pystache import TemplateSpec


class Basic(TestCase):

    """
    Test the view decorator.
    """

    def create_app(self):
        """Make a test app"""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.fm = FlaskMustache(self.app)
        return self.app

    def setup_view(self, *args, **kwargs):
        """Create a view and decorate it with our pystache view_route"""

        @self.fm.view_route(*args, **kwargs)
        class Example(TemplateSpec):

            """
            An example view
            """

            template = "{{stuff}}"

            def route(self, stuff):
                self.stuff = stuff

    def test_valid_response(self):
        """Test that the application gives a valid response for our test route"""
        # Arrange
        route = '/test/<stuff>'
        self.setup_view(route)

        # Act
        response = self.client.get(route.replace('<stuff>', 'stuff'))

        # Assert
        self.assert200(response)

    def test_valid_content_mustache_var(self):
        """Test that the application gives valid content for a template with a simple mustache var to set"""
        # Arrange
        route = '/test/<stuff>'
        self.setup_view(route)

        # Act
        response = self.client.get(route.replace('<stuff>', 'stuff'))

        # Assert
        self.assertEquals(response.data, "stuff")


class Decorator(TestCase):

    """
    Test the view decorator.
    """

    def create_app(self):
        """Make a test app"""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.fm = FlaskMustache(self.app)
        return self.app

    def setup_view(self, *args, **kwargs):
        """Create a view and decorate it with our pystache view_route"""

        @self.fm.view_route(*args, **kwargs)
        class Example(TemplateSpec):

            """
            An example view
            """

            template = "{{hello}}{{dynamic}}"

            def route(self, **kwargs):
                self.route_args = kwargs

            def hello(self):
                return "hello"

            def dynamic(self):
                return self.route_args.get('dynamic', '')

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


class RouteOptional(TestCase):

    """
    Test the view decorator without a route method.
    """

    def create_app(self):
        """Make a test app"""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.fm = FlaskMustache(self.app)
        return self.app

    def setup_view(self, *args, **kwargs):
        """Create a view and decorate it with our pystache view_route"""

        @self.fm.view_route(*args, **kwargs)
        class Example(TemplateSpec):

            """
            An example view
            """

            template = "{{hello}}"

            def hello(self):
                return "hello"

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


class RouteOptional404(TestCase):

    """
    Test the view decorator without a route method when a 404 occurs.
    """

    def create_app(self):
        """Make a test app"""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.fm = FlaskMustache(self.app)
        return self.app

    def setup_view(self, *args, **kwargs):
        """Create a view and decorate it with our pystache view_route"""

        @self.fm.view_error(404, *args, **kwargs)
        class Example404(TemplateSpec):

            """
            An example 404 view
            """

            template = "{{hello}}"

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


class Decorator404(TestCase):

    """
    Test the view decorator when a 404 occurs.
    """

    def create_app(self):
        """Make a test app"""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.fm = FlaskMustache(self.app)
        return self.app

    def setup_view(self, *args, **kwargs):
        """Create a view and decorate it with our pystache view_route"""

        @self.fm.view_error(404, *args, **kwargs)
        class Example404(TemplateSpec):

            """
            An example 404 view
            """

            template = "{{hello}}"

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
        self.fm = FlaskMustache(self.app)
        return self.app

    def setup_view(self, *args, **kwargs):
        """Create a view and decorate it with our pystache view_route"""

        @self.fm.view_route('/testexception', *args, **kwargs)
        class ExampleRaiseException(TemplateSpec):

            """
            An example view
            """

            template = "{{hello}}"

            def hello(self):
                raise Exception("testing")

        @self.fm.view_error(Exception, *args, **kwargs)
        class ExampleException(TemplateSpec):

            """
            An example Exception view
            """

            template = "{{hello}}{{dynamic}}"

            def route(self, **kwargs):
                self.route_args = kwargs

            def hello(self):
                return "hello exception"

            def dynamic(self):
                return self.route_args.get('dynamic', '')

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
        self.fm = FlaskMustache(self.app)
        return self.app

    def setup_view(self, *args, **kwargs):
        """Create a view and decorate it with our pystache view_route"""

        @self.fm.view_route('/testnotimplemented', *args, **kwargs)
        class ExampleRaiseNotImplemented(TemplateSpec):

            """
            An example view
            """

            template = "{{hello}}{{dynamic}}"

            def route(self, **kwargs):
                self.route_args = kwargs

            def hello(self):
                raise NotImplementedError("testing")

            def dynamic(self):
                return self.route_args.get('dynamic')

        @self.fm.view_error(NotImplementedError, 501, *args, **kwargs)
        class ExampleCustomCode(TemplateSpec):

            """
            An example Exception view
            """

            template = "{{hello}}"

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
