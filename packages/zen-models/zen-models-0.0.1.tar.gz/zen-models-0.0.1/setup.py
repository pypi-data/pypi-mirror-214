from setuptools import setup, find_packages


setup(
    name='zen-models',
    version='0.0.1',
    license='MIT',
    author="Ravi Shankar Vats",
    author_email='ravisvats@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    # url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='models zenerate naehas',
    install_requires=[
          'SQLAlchemy>=2.0.16',
      ],

)