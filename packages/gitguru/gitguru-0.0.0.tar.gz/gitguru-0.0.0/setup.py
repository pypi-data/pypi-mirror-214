from setuptools import setup, find_packages


VERSION = "0.0.0"


def read_requirements():
    with open("requirements.txt") as file:
        return list(file)


def get_long_description():
    with open("README.md", encoding="utf8") as file:
        return file.read()


setup(
    name="gitguru",
    description="",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Sébastien De Revière",
    url="https://github.com/sderev/gitguru",
    project_urls={
        "Documentation": "https://github.com/sderev/gitguru",
        "Issues": "http://github.com/sderev/gitguru/issues",
        "Changelog": "https://github.com/sderev/gitguru/releases",
    },
    license="Apache Licence, Version 2.0",
    version=VERSION,
    packages=find_packages(),
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
        ]
    },
    python_requires=">=3.8",
)

