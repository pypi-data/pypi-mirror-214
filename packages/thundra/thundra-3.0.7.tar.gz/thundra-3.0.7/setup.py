import codecs
import os.path
import subprocess

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


def get_git_revision_short_hash():
    try:
        return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()
    except:
        return "1"


def get_version():
    _hash = abs(hash(get_git_revision_short_hash())) % (10 ** 8)
    _version = get_main_version('catchpoint/_version.py')

    release_type = os.environ.get('RELEASE_TYPE', None)
    if ALPHA_RELEASE_TYPE == release_type:
        return _version + '.a.' + str(_hash)
    elif BETA_RELEASE_TYPE == release_type:
        return _version + '.b.' + str(_hash)
    elif RC_RELEASE_TYPE == release_type:
        return _version + '.rc.' + str(_hash)
    else:
        return _version


setup(name='thundra',
      version=get_version(),
      description='Catchpoint Python agent',
      long_description='Catchpoint Python agent',
      url='https://github.com/cp-trace-python',
      author='Catchpoint',
      author_email='python@catchpoint.io',
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
