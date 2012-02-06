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
    version='0.2.0',
    url='http://github.com/ahri/flask-mustache',
    license='AGPLv3',
    author='Adam Piper',
    author_email='adam@ahri.net',
    description='Mustache for Flask',
    long_description=__doc__,
    packages=['flaskext'],
    namespace_packages=['flaskext'],
    test_suite="nose.collector",
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask>=0.8',
    ],
    tests_require=[
        'Flask-Testing>=0.3',
        'pystache>=0.3.1',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
