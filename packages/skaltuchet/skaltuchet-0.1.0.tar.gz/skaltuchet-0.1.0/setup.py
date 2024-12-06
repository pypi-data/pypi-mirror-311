from setuptools import setup, find_packages

setup(
    name="skaltuchet",
    version="0.1.0",
    author="skaltuchet",
    description="A hilarious fake hacking script to prank your friends!",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/skaltuch",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "skaltuch = skaltuch.__main__:fake_hack",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

