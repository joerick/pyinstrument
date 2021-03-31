import sys
import subprocess, os, distutils
from setuptools import setup, find_packages


# pylint: disable=e1101
class CommandUtilities:
    def check_call(self, args, **popen_kwargs):
        self.announce('Running command: %s' % ' '.join(args), level=distutils.log.INFO)
        if not self.dry_run:
            subprocess.check_call(args, **popen_kwargs)


class BuildAndUploadCommand(distutils.cmd.Command, CommandUtilities):
    user_options = []
    def initialize_options(self): pass
    def finalize_options(self): pass
    def run(self):
        self.check_call(['rm', '-rf', 'dist'])
        self.check_call(['bin/build_js_bundle.py', '--force'])
        self.run_command('build')
        self.run_command('sdist')
        self.run_command('bdist_wheel')
        self.check_call([sys.executable + ' -m twine upload dist/*'], shell=True)

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()

setup(
    name="pyinstrument",
    packages=find_packages(),
    version="3.4.1",
    description="Call stack profiler for Python. Shows you why your code is slow!",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Joe Rickerby',
    author_email='joerick@mac.com',
    url='https://github.com/joerick/pyinstrument',
    keywords=['profiling', 'profile', 'profiler', 'cpu', 'time', 'sampling'],
    install_requires=['pyinstrument_cext>=0.2.2'],
    include_package_data=True,
    python_requires='>=3.6',
    entry_points={'console_scripts': ['pyinstrument = pyinstrument.__main__:main']},
    zip_safe=False,
    cmdclass={
        'build_and_upload': BuildAndUploadCommand,
    },
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Software Development :: Testing',
    ]
)
