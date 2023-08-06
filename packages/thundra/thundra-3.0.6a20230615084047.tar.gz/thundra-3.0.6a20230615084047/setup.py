import codecs
import os.path

from datetime import datetime
from setuptools import setup, find_packages

ALPHA_RELEASE_TYPE = 'alpha'
BETA_RELEASE_TYPE = 'beta'
RC_RELEASE_TYPE = 'rc'


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_main_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


def get_date_time_str():
    now = datetime.now() # current date and time
    return now.strftime("%Y%m%d%H%M%S")


def get_version():
    _date_time_str = get_date_time_str()
    _version = get_main_version('catchpoint/_version.py')

    release_type = os.environ.get('RELEASE_TYPE', None)
    if ALPHA_RELEASE_TYPE == release_type:
        return _version + '.a' + _date_time_str
    elif BETA_RELEASE_TYPE == release_type:
        return _version + '.b' + _date_time_str
    elif RC_RELEASE_TYPE == release_type:
        return _version + '.rc' + _date_time_str
    else:
        return _version


from setuptools.command.install import install
class CustomInstallCommand(install):
    """Customized setuptools install command - prints a friendly greeting."""
    def run(self):
        print ("Hello, developer, how are you? :")
        install.run(self)


setup(name='thundra',
      version=get_version(),
      description='Catchpoint Python agent',
      long_description='Catchpoint Python agent',
      cmdclass={
            'install': CustomInstallCommand,
      },
      url='https://github.com/cp-trace-python',
      author='Thundra',
      author_email='python@thundra.io',
      python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
      packages=find_packages(exclude=('tests', 'tests.*',)),
      install_requires=['requests>=2.16.0', 'opentracing>=2.0', 'wrapt>=1.10.11', 'simplejson', 'enum-compat',
                        'jsonpickle==1.3', 'websocket-client', 'python-dateutil', 'GitPython>=3.1.18', 'fastcounter>=1.1.0', 'pympler'],
      zip_safe=True,
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
      ],
      )
