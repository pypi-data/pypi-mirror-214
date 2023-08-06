
__version__ = "3.0.6.rc2023"


#patch
#minor
#major
# #semver

from pep440_rs import Version, VersionSpecifier




import os,codecs
from datetime import datetime

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


def get_version():
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


def get_release_version(release_scale):
    version_format = "{0}.{1}.{2}"
    _version = get_main_version('_version.py')
    current_version = Version(_version)
    if PATCH_RELEASE == release_scale:
        return version_format.format(current_version.major, current_version.minor, current_version.micro + 1)
    elif MINOR_RELEASE == release_scale:
        return version_format.format(current_version.major, current_version.minor + 1, 0)
    elif MAJOR_RELEASE == release_scale:
        return version_format.format(current_version.major + 1, 0, 0)
    else:
        raise Exception('RELEASE_SCALE environment is wrong!')






# 'git', 'commit', '-F',