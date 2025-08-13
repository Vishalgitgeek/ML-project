from setuptools import setup, find_packages

setup(
    name="mlproject",  # any name you like
    version="0.1",
    author="Vishal Kumar",
    author_email="your.email@example.com",
    description="End-to-end ML project with Django integration",
    packages=find_packages(),  # finds 'src' and submodules
    package_dir={"": "."},  # root dir is the base for packages
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "xgboost",
        "catboost",
        "django"
    ],
)
