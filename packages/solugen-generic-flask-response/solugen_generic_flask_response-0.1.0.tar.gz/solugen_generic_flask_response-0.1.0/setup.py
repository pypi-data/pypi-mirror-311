from setuptools import setup, find_packages

setup(
    name="solugen_generic_flask_response",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Flask>=2.0.0",
    ],
    description="A simple utility to create JSON success/error responses for Flask.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/generic-response/",
    author="Your Name",
    author_email="your_email@example.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
