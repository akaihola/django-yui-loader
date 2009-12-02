__doc__ = """

YUI_include -- YUI Loader as Django middleware

(c) 2008-2009 Antti Kaihola and individual contributors
              akaihol+django@ambitone.com

License: BSD, see the file LICENSE for details

See README.rst for documentation
"""

import ez_setup
ez_setup.use_setuptools()
from setuptools import setup

setup(
    name='django-yui-loader',
    author='Antti Kaihola',
    author_email='akaihol+django@ambitone.com',
    maintainer='Antti Kaihola',
    maintainer_email='akaihol+django@ambitone.com',
    version='0.3',
    url='http://github.com/akaihola/django-yui-loader',
    packages=['yui_loader'],
    description=('Server-side middleware which implements some of the '
                 'functionality in the Yahoo User Interface Loader '
                 'component.'),
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ]
)
