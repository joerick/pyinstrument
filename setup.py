import sys
import setuptools, subprocess, os, distutils
import setuptools.command.build_py
from setuptools import setup, find_packages


HTML_RENDERER_DIR = 'html_renderer'
JS_BUNDLE = 'pyinstrument/renderers/html_resources/app.js'

# pylint: disable=e1101
class CommandUtilities:
    def check_call(self, args, **popen_kwargs):
        self.announce('Running command: %s' % ' '.join(args), level=distutils.log.INFO)
        if not self.dry_run:
            subprocess.check_call(args, **popen_kwargs)


class BuildPyCommand(setuptools.command.build_py.build_py, CommandUtilities):
    """Custom build command."""

    def run(self):
        '''compile the JS, then run superclass implementation'''

        # when installing from tarball, the JS is already built, so don't try to build it again
        js_source_mtime = 0
        for dirpath, _, filenames in os.walk(HTML_RENDERER_DIR):
            for filename in filenames:
                file = os.path.join(dirpath, filename)
                js_source_mtime = max(js_source_mtime, os.path.getmtime(file))
        
        js_bundle_is_up_to_date = (os.path.exists(JS_BUNDLE)
                                   and os.path.getmtime(JS_BUNDLE) >= js_source_mtime)

        if not js_bundle_is_up_to_date:
            if subprocess.call(['npm', '--version']) != 0:
                raise RuntimeError('npm is required to build the HTML renderer.')

            self.check_call(['npm', 'ci'], cwd=HTML_RENDERER_DIR)
            self.check_call(['npm', 'run', 'build'], cwd=HTML_RENDERER_DIR)

            self.copy_file(HTML_RENDERER_DIR+'/dist/js/app.js', JS_BUNDLE)

        setuptools.command.build_py.build_py.run(self)


class HTMLDevServerCommand(distutils.cmd.Command, CommandUtilities):
    description = 'run the HTML renderer dev server'
    user_options = []
    def initialize_options(self): pass
    def finalize_options(self): pass

    def run(self):
        subprocess.check_call(['npm', 'run', 'serve'], cwd=HTML_RENDERER_DIR)


class BuildAndUploadCommand(distutils.cmd.Command, CommandUtilities):
    user_options = []
    def initialize_options(self): pass
    def finalize_options(self): pass
    def run(self):
        self.check_call(['rm', '-rf', 'dist'])
        self.check_call(['rm', '-rf', JS_BUNDLE])
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
        'build_py': BuildPyCommand,
        'dev_server': HTMLDevServerCommand,
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
