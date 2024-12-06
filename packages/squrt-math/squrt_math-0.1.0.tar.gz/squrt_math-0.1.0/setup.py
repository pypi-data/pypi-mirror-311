from setuptools import setup,find_packages

setup(
    name="squrt_math",  # Package name
    version="0.1.0",           # Version
    author="sujitmalga",
    author_email="sujithmalga@gmail.com",
    description="A custom package for demonstration purposes.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",  # GitHub repo URL
    packages=find_packages(),  # Automatically find package directories
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires="<=3.13.0",  # Minimum Python version
    install_requires=[],      # List dependencies here
)