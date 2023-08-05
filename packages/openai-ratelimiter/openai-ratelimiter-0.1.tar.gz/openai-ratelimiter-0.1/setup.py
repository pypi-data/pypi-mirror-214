from setuptools import find_packages, setup

setup(
    name="openai-ratelimiter",
    version="0.1",
    packages=find_packages(where="openai_ratelimiter"),
    description="A Python module that provides rate limiting capabilities for the OpenAI API, utilizing Redis as a caching service. It helps to manage API usage to avoid exceeding OpenAI's rate limits.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/blaze-Youssef/openai-ratelimiter",
    author="Youssef Benhammouda",
    author_email="youssef@benhammouda.ma",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    install_requires=[
        x for x in open("./requirements.txt", "r+").readlines() if x.strip()
    ],
)
