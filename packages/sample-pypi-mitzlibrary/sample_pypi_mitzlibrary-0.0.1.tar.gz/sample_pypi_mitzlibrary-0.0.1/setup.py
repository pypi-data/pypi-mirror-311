import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sample-pypi-mitzlibrary",  # Replace with a unique name for your library
    version="0.0.1",  # Initial version
    author="Mithun Chandrasekar",  # Your name
    author_email="mithunxchandrasekar1@gmail.com",  # Your email
    description="A sample Python library to demonstrate PyPI publishing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MithunChandrasekar/example-pkg-mitz",  # URL to your repository
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
