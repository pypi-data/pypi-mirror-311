import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="enable-log-streaming-MithunChandrasekar", 
    version="0.0.2",
    author="Mithun Chandrasekar",
    author_email="mithunxchandrasekar1@gmail.com",
    description="A library to enable log streaming for Elastic Beanstalk environments.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MithunChandrasekar/enable-log-streaming-MithunChandrasekar",  
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
