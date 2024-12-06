from setuptools import setup, find_packages
import os

# Get the path to the `package_version.txt` file
version_file = os.path.join(
    os.path.dirname(__file__), "app_monitoring", "package_version.txt"
)

# Read the version from the VERSION file
with open(version_file) as f:
    version = f.read().strip()

setup(
    name="app_monitoring",
    version=version,
    description="A to monitoring my app.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Koi",
    author_email="your.email@example.com",
    url="http://gitea:8000/datlt4/fortifai_monitoring",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "app_monitoring=app_monitoring.cli:monitoring",
        ],
    },
    package_data={
        "app_monitoring": ["package_version.txt"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
