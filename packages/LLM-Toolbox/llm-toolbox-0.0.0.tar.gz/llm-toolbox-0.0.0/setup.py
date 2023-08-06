from setuptools import setup


with open("README.md", encoding="UTF-8") as file:
    readme = file.read()

setup(
    name="llm-toolbox",
    version="0.0.0",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="sderev",
)
