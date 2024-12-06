from setuptools import setup, find_packages

setup(
    name="care_sm_toolkit",  # Normalized project name to comply with PEP 625
    version="0.1.3",
    packages=find_packages(),
    author="Pablo Alarcón Moreno",
    author_email="pabloalarconmoreno@gmail.com",
    url="https://github.com/CARE-SM/CARE-SM-Toolkit",
    description="A toolkit for CARE-SM data transformation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    keywords=["FAIR-in-a-box", "Fiab", "CARE-SM", "Toolkit", "EJP-RD", "ERDERA"],
    classifiers=[
        "Development Status :: 3 - Alpha",  
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.8", 
    install_requires=[
        "pandas>=1.0.0",  
        "numpy>=1.20.0",
    ],
    project_urls={
        "Source": "https://github.com/CARE-SM/CARE-SM-Toolkit",
        "Bug Tracker": "https://github.com/CARE-SM/CARE-SM-Toolkit/issues",
    },
)