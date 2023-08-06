from setuptools import setup, find_packages


setup(
    name='zen_models',
    version='0.0.2',
    description="The zen models Python package is an internal package for zenerate team. It contains all the models "
                "which will be common to different microservices and could be used in all of them",
    license='MIT',
    author="Ravi Shankar Vats",
    author_email='ravisvats@gmail.com',
    packages=['zen_models'],
    keywords='models zenerate naehas',
    install_requires=[
          'SQLAlchemy',
      ]
)
