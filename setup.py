import os
from setuptools import setup, find_packages


def get_version():
    filename = 'bot/version.txt'
    if os.path.exists(filename):
        with open(os.path.join(os.path.dirname(__file__), filename)) as f:
            return f.read()
    return '0.0.0'

setup(
    name='slack-xlrelease-app',
    version=get_version(),
    packages=find_packages(exclude=[]),
    url='https://github.com/xebialabs-community/slack-xlrelease-app',
    license='MIT',
    author='Mayur Patel',
    description='Slack App for XL Release'
)
