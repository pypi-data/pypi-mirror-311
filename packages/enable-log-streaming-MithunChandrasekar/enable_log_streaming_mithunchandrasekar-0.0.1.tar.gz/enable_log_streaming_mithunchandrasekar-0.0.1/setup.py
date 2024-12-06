import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="enable-log-streaming-MithunChandrasekar",  # Replace with a unique name
    version="0.0.1",
    author="Mithun Chandrasekar",
    author_email="mithunxchandrasekar1@gmail.com",
    description="A library to enable log streaming for Elastic Beanstalk environments.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/enable-log-streaming",  # Update with your repository URL
    packages=setuptools.find_packages(),
    install_requires=[
        "boto3>=1.20.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
