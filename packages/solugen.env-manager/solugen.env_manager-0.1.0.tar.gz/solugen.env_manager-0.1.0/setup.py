from setuptools import setup, find_packages

setup(
    name="solugen.env_manager",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-dotenv==1.0.1",
    ],
    description="A Python library to manage environment variables",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/solugenai/env-manager",
    author="Elad Laor",
    author_email="elad.l@solugen.ai",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
)
