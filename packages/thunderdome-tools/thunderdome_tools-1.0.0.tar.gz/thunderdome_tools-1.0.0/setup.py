from setuptools import setup, find_packages

setup(
    name="thunderdome-tools",
    version="1.0.0",
    description="A utility package for standardized API configurations and tools.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jake Mayer",
    author_email="jakemay3r@gmail.com",
    url="https://github.com/thunderdomeai/thundertools",  # GitHub repo
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "langchain>=0.0.1",
        "json>=0.0.1",
        "typing>=0.0.1",
        "datetime>=0.0.1",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
