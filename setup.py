from setuptools import setup, find_packages
 
setup(
    name="pyinstrument",
    version="0.1",
    long_description=open('README.md').read(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)