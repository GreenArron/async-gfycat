import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="async-gfycat",
    version="1.0.0",
    author="GreenArron",
    description="An async wrapper for Gfycat API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GreenArron/async-gfycat",
    project_urls={
        "Bug Tracker": "https://github.com/GreenArron/async-gfycat/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    requires=['aiohttp'],
    package_dir={"": "async_gfycat"},
    packages=setuptools.find_packages(where="async_gfycat"),
    python_requires=">=3.7",

)