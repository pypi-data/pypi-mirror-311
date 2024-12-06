import setuptools

with open("README", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swapoc", # Replace with your own PyPI username(id)
    version="0.0.5",
    author="Jihu Kim",
    author_email="boj.jerry@gmail.com",
    description="for rce",
    long_description=long_description,
    url="https://github.com/swap-dh/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
