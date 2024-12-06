from setuptools import setup, find_packages
import pathlib

# Path to the directory containing README.md
current_dir = pathlib.Path(__file__).parent

# Read the long description from README.md
long_description = (current_dir / "README.md").read_text()

setup(
    name="django-notebook-config",
    version="0.1.1",
    description="A utility to easily use Django in IDEs Jupyter Notebooks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Abdul Wajed Khan",
    author_email="wajed.abdul.khan@gmail.com",
    license="MIT",
    url="https://github.com/WazedKhan/django-notebook-config",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
    ],
    keywords="django jupyter notebook development helper debugger",
)
