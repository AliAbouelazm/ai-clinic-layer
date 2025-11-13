from setuptools import setup, find_packages

setup(
    name="clinix-ai",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.3.0",
        "SQLAlchemy>=2.0.0",
        "streamlit>=1.28.0",
        "python-dotenv>=1.0.0",
        "matplotlib>=3.7.0",
        "joblib>=1.3.0",
    ],
)


