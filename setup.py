from setuptools import setup, find_packages

setup(
    name='coded-blockchain-query',
    version='0.1.0',
    author='Dineth Mudugamuwa Hewage',
    author_email='dineth.m@unb.ca',
    description='A project for implementing coded blockchain based range queries on historical data.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'Flask==2.0.1',
        'numpy==1.21.0',
        'pandas==1.3.0',
        'requests==2.25.1',
        'pytest==6.2.4',
        'pycryptodome==3.10.1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)