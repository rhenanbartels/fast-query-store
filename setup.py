import setuptools
from os import path

here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')


install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

setuptools.setup(
    name="fast-query-store",
    version="0.0.1.dev0",
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
    install_requires=install_requires,
    dependency_links=dependency_links,
)
