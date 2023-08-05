from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="Flask-PyTelegramBotAPI",
    version='0.0.1',
    author='kuzmichus',
    packages=['src/flask_pytelegrambotapi'],
    install_requires=["Flask < 3"],
)