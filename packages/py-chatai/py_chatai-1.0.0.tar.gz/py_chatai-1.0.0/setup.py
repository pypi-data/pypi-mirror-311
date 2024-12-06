from setuptools import setup, find_packages

setup(
    name="py-chatai",
    version="1.0.0",
    description="A simple Python library for interacting with ChatGPT models.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="MohamedLunar",
    author_email="contact.mohamedlunardev@gmail.com",
    url="https://github.com/mohamedlunar/pychatai",
    packages=find_packages(),
    install_requires=["openai"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
