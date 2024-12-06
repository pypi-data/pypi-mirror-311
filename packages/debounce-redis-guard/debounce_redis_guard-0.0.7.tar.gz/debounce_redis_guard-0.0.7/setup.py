from setuptools import setup, find_packages

setup(
    name="debounce_redis_guard",
    version="0.0.7",
    packages=find_packages(),
    install_requires=[],
    author="Chathura Deepana Herath",
    author_email="chathuradeepana7@gmail.com",
    description="A Python library for debouncing requests with support for multiple workers.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cdeepana/debounce_redis_guard",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Fixed classifier here
        # "Framework :: Redis",
    ],
    python_requires='>=3.6',
)