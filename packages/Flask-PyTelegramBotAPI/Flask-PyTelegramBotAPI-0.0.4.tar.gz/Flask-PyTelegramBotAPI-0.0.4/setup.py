from setuptools import setup, find_packages

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="Flask-PyTelegramBotAPI",
    url='https://github.com/kuzmichus/flask-pytelegrambotapi',
    version='0.0.4',
    author='kuzmichus',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=['pytelegrambotapi', "Flask < 3"],
    description='Интеграция Flask c PyTelegramBotAPI'
)