from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bindry",
    use_scm_version={
        "write_to": "src/bindry/_version.py",
    },
    author="Jason",
    author_email="hcleung.ca+github@gmail.com",
    description="Elegant Python Dependency Injection with Profile-Aware Configuration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hcleungca/bindry",
    project_urls={
        "Bug Tracker": "https://github.com/hcleungca/bindry/issues",
        "Documentation": "https://bindry.readthedocs.io/",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pyyaml>=5.1",
        "python-dotenv>=0.19.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=22.0",
            "isort>=5.0",
            "flake8>=3.9",
            "mypy>=0.910",
            "tox>=3.24",
        ],
    },
)