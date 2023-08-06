from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='random-otp',
    version='1.0.0',
    author='Abhijith',
    author_email='abhis@tuta.io',
    description='A Python package for generating random OTPs',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'pycryptodome>=3.10.1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'random-otp-generator=random_otp.generator:main',
        ],
    },
)