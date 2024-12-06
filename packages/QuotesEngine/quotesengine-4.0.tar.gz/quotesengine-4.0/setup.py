from setuptools import setup, find_packages

setup(
    name="QuotesEngine",
    version="4.0",
    description="A Python library to display some random motivation quotes.",
    author="Sridharan",
    author_email="sridharansri2312@gmail.com",
    packages=find_packages(),
    install_requires=[],
    long_description=open("README.md", encoding="utf-8").read(),    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
