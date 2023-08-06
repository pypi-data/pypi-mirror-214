from setuptools import setup
import setuptools

setup(
    name="bc-acc-dup",
    version='1.0.0',
    author="CintagramABP",
    description="battle cats account duplicator",
    long_description="battle cats account duplicator",
    url="",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[
        "colored==1.4.4",
        "tk",
        "python-dateutil",
        "requests",
        "pyyaml",
        "aiohttp"
    ],
    flake8={"max-line-length": 160},
)