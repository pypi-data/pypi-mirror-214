from setuptools import find_packages, setup

setup(
    name='photoflow',
    version='2.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask>2.2',
        'Flask-Migrate',
        'Flask-Wtf',
        'Flask-Sqlalchemy>=3.0.0',
        'Flask-Login',
        'Sqlalchemy-utils',
        'Wtforms-Sqlalchemy',
        'Pillow>6.0.0',
        'toml',
    ],
)
