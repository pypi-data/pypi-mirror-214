from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    # name="titanic_model",
    name="PEC_project_Diego_Benavent",
    version="0.1.1",
    description="A training pipeline for a model to predict if a passenger survived the Titanic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Diego Benavent",
    packages=find_packages(),
    install_requires=[
        "scikit-learn==1.2.2",
        "pandas==2.0.2",
        "flask==2.3.2",
        "requests==2.31.0",
    ],
)
