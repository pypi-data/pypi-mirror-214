from setuptools import setup, find_packages

setup(
    name="dataintellect",
    version="0.0.0",
    description="Initial package",
    author="Data Intellect",
    author_email="dataanalytics@dataintellect.com",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[]
)