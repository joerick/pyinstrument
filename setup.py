from setuptools import setup

setup(
    name="pyinstrument",
    packages=['pyinstrument'],
    version="2.3.0",
    description="A call stack profiler for Python. Inspired by Apple's Instruments.app",
    author='Joe Rickerby',
    author_email='joerick@mac.com',
    url='https://github.com/joerick/pyinstrument',
    keywords=['profiling', 'profile', 'profiler', 'cpu', 'time', 'sampling'],
    install_requires=['pyinstrument_cext>=0.2.0'],
    include_package_data=True,
    entry_points={'console_scripts': ['pyinstrument = pyinstrument.__main__:main']},
    zip_safe=False,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Software Development :: Testing',
    ]
)
