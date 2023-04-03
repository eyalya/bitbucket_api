from setuptools import setup

from bitbucket import __version__

setup(
    name='bitbucket_api',
    version=__version__,

    url='https://github.com/eyalya/bitbucket_api',
    author='Eyal Yaish',
    author_email='eyalyaish@gmail.com',

    py_modules=['bitbucket_api'],
    install_requires=[
        'requests'
    ]
)