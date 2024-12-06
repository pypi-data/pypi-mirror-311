from setuptools import setup, find_packages

setup(
    name="tensorama",  # Your library name
    version="0.1.1",  # Version number
    description="A simple library to help people",
    author="Clonitty",
    author_email="teamclonitty@gmail.com",
    packages=find_packages(),  # Automatically find sub-packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7, <4',
)
