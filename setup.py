import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="async-gfycat",
    version="1.0.2",
    author="GreenArron",
    description="An async wrapper for Gfycat API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GreenArron/async-gfycat",
    project_urls={
        "Bug Tracker": "https://github.com/GreenArron/async-gfycat/issues",
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    keywords=['gfycat', 'api', 'async'],
    install_requires=requirements,
    packages=setuptools.find_packages(),
    python_requires=">=3.8.0",

)