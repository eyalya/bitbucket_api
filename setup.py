from setuptools import setup

setup(
    name='bitbucket_api',
    version="dev",

    url='https://github.com/eyalya/bitbucket_api',
    author='Eyal Yaish',
    author_email='eyalyaish@gmail.com',
    license='MIT',

    packages=['bitbucket_api'],
    install_requires=[
        "requests",
    ]
)