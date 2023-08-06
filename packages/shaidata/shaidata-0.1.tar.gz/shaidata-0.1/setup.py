# setup.py
from glob import glob
from os.path import basename, splitext
from setuptools import setup, find_packages
import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shaidata", 
    version="0.1",
    description='Shinhan AI Data Pipeline',
    author='Shinhan AI',    
    long_description=long_description,
    long_description_content_type="text/markdown",    
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    python_requires=">=3.9.13",
    install_requires=[
        'bcrypt==4.0.1',
        'certifi==2023.5.7',
        'cffi==1.15.1',
        'charset-normalizer==3.1.0',
        'colorlog==6.7.0',
        'croniter==1.3.15',
        'crypto==1.4.1',
        'cryptography==41.0.1',
        'funcy==2.0',
        'greenlet==2.0.2',
        'idna==3.4',
        'inflect==6.0.4',
        'Naked==0.1.32',
        'paramiko==3.2.0',
        'pycparser==2.21',
        'pycryptodome==3.18.0',
        'pydantic==1.10.8',
        'PyMySQL==1.0.3',
        'PyNaCl==1.5.0',
        'python-crontab==2.7.1',
        'python-dateutil==2.8.2',
        'PyYAML==6.0',
        'requests==2.31.0',
        'shellescape==3.8.1',
        'six==1.16.0',
        'sqlacodegen==2.3.0.post1',
        'SQLAlchemy==1.4.48',
        'typing_extensions==4.6.2',
        'urllib3==2.0.2'
    ]
)
