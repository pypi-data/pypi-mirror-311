from setuptools import setup, find_packages

setup(
    name="isJem3a",
    version="1.0.0",
    description="A package to check if tomorrow is Friday",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="chkoupey",
    author_email="bounemeryannis@gmail.com",
    url="https://github.com/bounyan/isJem3a",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'isJem3a=isJem3a.check:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
