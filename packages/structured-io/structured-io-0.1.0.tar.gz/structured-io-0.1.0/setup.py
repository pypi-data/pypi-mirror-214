import setuptools


if __name__ == "__main__":
    with open("README.md", "r") as readme:
        long_description = readme.read()
    setuptools.setup(
        name="structured-io",
        version="0.1.0",
        author="nocturn9x",
        author_email="nocturn9x@nocturn9x.space",
        description="An experimental structured concurrency framework",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://example.com",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
            "License :: OSI Approved :: Apache Software License",
        ],
        python_requires=">=3.8",
    )
