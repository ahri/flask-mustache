# coding: utf-8

from flask import Flask
from flaskext.testing import TestCase
from pystache import View

import sys
sys.path.append("flaskext")
from mustache import viewroute

class Decorator(TestCase):

    """
    Test the view decorator
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
