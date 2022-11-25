from distutils.core import setup

setup(
    version="1.0.0",
    name="proxyscrape-api-wrapper",
    description="A simple Proxyscrape API wrapper",
    packages=[
        'proxyscrape',
    ],
    install_requires=[
        'requests>=2.27.1',
        'tinydb>=4.7.0'
    ]
)