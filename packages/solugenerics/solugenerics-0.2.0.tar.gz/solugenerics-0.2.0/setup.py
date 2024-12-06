from setuptools import setup, find_packages

setup(
    name="solugenerics",
    version="0.2.0",
    packages=find_packages(),  # Automatically discovers 'solugeneric/' and its sub-packages
    install_requires=[
        "Flask>=2.0.0",
        "python-dotenv==1.0.1",
    ],
    description="Reusable tools for Solugen workers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/solugeneric/",
    author="Your Name",
    author_email="your_email@example.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
