from setuptools import setup, find_packages

packages = find_packages(exclude=["examples"])

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="EMIS",
    version='1.0.0',
    author='Vishal',
    author_email='vishallindan170@gmail.com',
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="UNLICENSED",
    packages=packages,
    url='',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    install_requires=[
    ],
    extras_require={
    }
)
