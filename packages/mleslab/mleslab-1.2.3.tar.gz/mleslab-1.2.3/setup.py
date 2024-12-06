from setuptools import setup, find_packages

setup(
    name="mleslab",                  # Your package name
    version="1.2.3",                 # Initial version
    description="A package to load and return program content.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/mleslab",  # Replace with your GitHub repo link
    license="MIT",                   # Or choose the appropriate license
    packages=find_packages(),        # Automatically find packages
    include_package_data=True,       # Include non-Python files
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",          # Minimum Python version required
)
