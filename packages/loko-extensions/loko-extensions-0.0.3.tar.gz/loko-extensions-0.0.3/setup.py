import setuptools,os

def get_requirements():
    return [x for x in open("./requirements.txt").read().split("\n") if not x.startswith("pkg_resources")]

def get_long_description() -> str:

    readme_filepath = os.path.join(os.path.dirname(__file__), "README.md")
    with open(readme_filepath) as f:
        return f.read()

import json
ppom=json.load(open("./ppom.json"))
version=ppom['version']

setuptools.setup(
    name="loko-extensions",
    version=version,
    author="Live Tech",
    author_email="f.dantonio@ilivetech.it",
    description="A framework for Loko extensions",
    long_description=get_long_description(),
    python_requires='>3.5.0',
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=get_requirements()

)