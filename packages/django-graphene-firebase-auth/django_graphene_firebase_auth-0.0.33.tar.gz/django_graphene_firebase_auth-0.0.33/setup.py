import os
from setuptools import setup


README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
VERSION = '0.0.33'

setup(
    name='django_graphene_firebase_auth',
    version=VERSION,
    author='Eba Alemayehu',
    author_email='ebaalemayhu3@gmail.com',
    description=(
        "Authentication provider for graphene-django and Google Firebase's "
        "Authentication service."
    ),
    license='MIT',
    keywords='graphene django firebase auth',
    url='https://github.com/eba-alemayehu/graphene-django-firebase-auth',
    packages=['firebase_auth'],
    install_requires=['django', 'firebase-admin'],
    long_description=README,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ],
)
