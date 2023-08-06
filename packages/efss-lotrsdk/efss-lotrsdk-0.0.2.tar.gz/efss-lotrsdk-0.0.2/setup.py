from setuptools import setup, find_packages

setup(
    name="efss-lotrsdk",
    version="0.0.2",
    packages=find_packages(),
    author="Emmanuel Felipe",
    author_email="hi@emmanuel.cloud",
    description="A SDK for the-one-api.dev API updated ",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.11',
    install_requires=[
        "requests",
        "pytest",
    ],
)