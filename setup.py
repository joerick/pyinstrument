from setuptools import setup, find_packages
 
setup(
    name="pyinstrument",
    version="0.1",
    description="A Python profiler that records the call stack of the executing code, instead of just the final function in it. Inspired by Apple's Instruments.app",
    long_description=open('README.md').read(),
    packages=['pyinstrument'],
    include_package_data=True,
    zip_safe=False,
)