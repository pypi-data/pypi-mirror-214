from setuptools import setup, find_packages

with open("README.md", "r") as file:
    readme_content = file.read()

setup(
    name="shopee-api-wrapper",
    version="0.1.0",
    license="MIT License",
    author="Marcuth",
    long_description=readme_content,
    long_description_content_type="text/markdown",
    author_email="marcuth2006@gmail.com",
    keywords="amazon affiliate scraper",
    description="A simple library that communicates with the Shopee website API.",
    packages=["shopee_api"] + [ "shopee_api/" + x for x in find_packages("shopee_api") ]
)