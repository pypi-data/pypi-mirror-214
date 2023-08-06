import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="bio2csv",
    version="0.0.1",
    author="Andrew Gao",
    author_email="gaodrew@stanford.edu",
    description="the easiest way to download many articles from biorxiv",
    long_description=long_description, # don't touch this, this is your README.md
    long_description_content_type="text/markdown",
    url="https://github.com/andrewgcodes",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)