"""
Flask-Mustache
--------------

Flask mustache integration.

Links
`````

* `development version
  <http://github.com/ahri/flask-mustache>`_

"""
from setuptools import setup

setup(
    name='Flask-Mustache',
    version='0.4.1',
    url='http://github.com/ahri/flask-mustache',
    license='MIT',
    author='Adam Piper',
    author_email='adam@ahri.net',
    description='Mustache for Flask',
    long_description=__doc__,
    test_suite="nose.collector",
    zip_safe=False,
    platforms='any',
    py_modules=['flask_mustache'],
    install_requires=[
        'Flask',
    ],
    tests_require=[
        'Flask-Testing',
        'pystache',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
