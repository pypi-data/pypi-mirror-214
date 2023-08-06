import codecs
import os

from datetime import datetime
from setuptools import setup, find_packages

ALPHA_RELEASE_TYPE = 'alpha'
BETA_RELEASE_TYPE = 'beta'
RC_RELEASE_TYPE = 'rc'

PATCH_RELEASE = 'patch'
MINOR_RELEASE = 'minor'
MAJOR_RELEASE = 'major'


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


def get_release_version(release_scale):
    version_format = "{0}.{1}.{2}"
    _version = get_main_version('catchpoint/_version.py')

    tokens = _version.split('.')
    if not tokens or len(tokens) < 3:
        raise Exception('Version format is wrong!')
    major = int(tokens[0])
    minor = int(tokens[1])
    patch = int(tokens[2])
    if PATCH_RELEASE == release_scale:
        return version_format.format(major, minor, patch + 1)
    elif MINOR_RELEASE == release_scale:
        return version_format.format(major, minor + 1, 0)
    elif MAJOR_RELEASE == release_scale:
        return version_format.format(major + 1, 0, 0)
    else:
        raise Exception('RELEASE_SCALE environment is wrong!')


def get_version():
    print(".......................................")
    print(".......................................")
    print(".......................................")
    print("def get_version():")
    print(".......................................")
    _date_time_str = get_date_time_str()

    release_scale = os.environ.get('RELEASE_SCALE', None)
    if release_scale is None:
        raise Exception('RELEASE_SCALE environment should be provided!')

    release_version = get_release_version(release_scale)
    release_type = os.environ.get('RELEASE_TYPE', None)
    if ALPHA_RELEASE_TYPE == release_type:
        return release_version + '.a' + _date_time_str
    elif BETA_RELEASE_TYPE == release_type:
        return release_version + '.b' + _date_time_str
    elif RC_RELEASE_TYPE == release_type:
        return release_version + '.rc' + _date_time_str
    else:
        return release_version



from setuptools.command.install import install
class CustomInstallCommand(install):
    def run(self):
        print(".......................................")
        print(".......................................")
        print(".......................................")
        print("CustomInstallCommand :")
        print(".......................................")
        import subprocess
        install.run(self)
        print(".......................................")
        release_version = get_version()
        print(release_version)
        print(".......................................")
        print(subprocess.call(["git", "tag", release_version]))
        print(subprocess.call(["git", "push", "origin", release_version]))


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
      install_requires=['requests>=2.16.0', 'opentracing>=2.0', 'wrapt>=1.10.11', 'simplejson', 'enum-compat', 'pep440_rs',
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
