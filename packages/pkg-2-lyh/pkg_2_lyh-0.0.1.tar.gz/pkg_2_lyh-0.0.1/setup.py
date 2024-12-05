import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pkg-2-lyh",
    version="0.0.1",
    author="Yihan Lin",
    author_email="22373442@buaa.edu.cn",
    description="A small example package which depend on pkg-1-lyh",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pkg-1-lyh",
    ],
)
