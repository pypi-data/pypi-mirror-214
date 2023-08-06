from setuptools import setup
from setuptools import find_packages
import os

def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()

setup(
    name='pyconnectwise',
    version='0.2.4',
    license='gpl-3.0',
    author="Health IT",
    author_email='dev@healthit.com.au',
    description='A full-featured Python client for the ConnectWise API\'s',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/HealthITAU/pyconnectwise',
    download_url='https://github.com/HealthITAU/pyconnectwise/archive/refs/tags/0.2.4.tar.gz',
    keywords=['ConnectWise', 'Manage', 'Automate', 'API', 'Python', 'Client', 'Annotated', 'Typed', 'MSP'],
    install_requires=[
          'requests',
          'pydantic',
          'jinja2'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',  
        'Intended Audience :: Developers',   
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',  
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.10',
    ],
    package_dir = {"":"src"},
    packages = find_packages(where="src"),
    python_requires = ">=3.10"
)