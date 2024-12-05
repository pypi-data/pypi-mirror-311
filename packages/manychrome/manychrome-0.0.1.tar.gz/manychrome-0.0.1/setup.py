from setuptools import setup, find_packages

setup(
    name="manychrome",
    version="0.0.1",
    author="Maria Wenner",
    author_email="mail@neurosystems.co",
    description="A simple package make life easier when working with text from the CLI.",
    packages=find_packages(),
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent"
    ],
    python_requires='>=3.8',
    homepage = "https://github.com/NeurosystemsCo/manychrome",
    issues = "https://github.com/NeurosystemsCo/manychrome/issues"
)
