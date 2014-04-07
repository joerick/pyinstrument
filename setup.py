from setuptools import setup, find_packages
 
setup(
    name="pyinstrument",
    version="0.5",
    description="A call stack profiler for Python. Inspired by Apple's Instruments.app",
    long_description=open('README.md').read(),
    packages=['pyinstrument'],
    include_package_data=True,
    zip_safe=False,
)