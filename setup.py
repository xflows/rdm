import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='python-rdm',
    version='0.3.6',
    packages=['rdm'],
    include_package_data=True,
    install_requires=[
        'PyMySQL',
        'psycopg2-binary',
        'liac-arff',
        'Orange3>=3.24.1'
    ],
    # only for documentation building
    extras_require={'dev': ['Sphinx', 'sphinx_rtd_theme']},
    license='MIT License',
    description='Relational data mining in python',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/xflows/rdm',
    author='Anze Vavpetic',
    author_email='anze.vavpetic@ijs.si',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Prolog',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries'
    ],
)
