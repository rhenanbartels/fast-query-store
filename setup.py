import setuptools
from os import path

__version__ = "0.0.3.dev0"

here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setuptools.setup(
    name="fast-query-store",
    version="0.0.3.dev0",
    author="Rhenan and Turicas",
    author_email="rhenan.bartels@gmail.com",
    description="A Fast Backend API for database queries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rhenanbartels/fast-query-store",
    project_urls={
        "Bug Tracker": "https://github.com/rhenanbartels/fast-query-store/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    python_requires=">=3.8",
    install_requires=[
        "aiofiles==0.6.0",
        "click==7.1.2",
        "fastapi==0.63.0",
        "fastapi-cache2==0.1.3.4",
        "SQLAlchemy==1.4.13",
        "uvicorn[standard]",
    ],
)
