from setuptools import setup, find_packages

setup(
    name="ekiti",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.0.0",
        "pydantic>=2.0.0",
        "pyyaml>=6.0",
        "sqlmodel>=0.0.8",
        "python-dotenv>=1.0.0"
    ],
    entry_points={
        "console_scripts": [
            "ekiti=ekiti.cli.main:app",
        ],
    },
    python_requires=">=3.8",
)
