from setuptools import setup

setup(
    name='slack-xlrelease-app',
    version='0.0.1',
    packages=['bot', 'bot.db', 'bot.slack', 'bot.helper', 'bot.dialogs', 'bot.messages', 'bot.xlrelease',
              'bot.exceptions'],
    url='https://github.com/xebialabs-community/slack-xlrelease-app',
    license='MIT',
    author='Mayur Patel',
    author_email='no-reply@xebialabs.com',
    description='Slack App for XL Release'
)
