import codecs, re, site, sys, shutil, os
from setuptools import setup, Extension

def get_version(version_file):
    with codecs.open(version_file, 'r') as fp:
        contents = fp.read()
    match = re.search(r"^__version__ = '([^']+)'", contents, re.M)
    if match:
        return match.group(1)
    raise RuntimeError("Unable to find version string")

site.ENABLE_USER_SITE = "--user" in sys.argv[1:]

VERSION = get_version(r'src\mhi\psout\__init__.py')

with open("README.md") as f:
    long_description = f.read()

if os.path.exists(r'Release\CurveFile.dll'):
    print(r"*** Copying CurveFile.dll to src\mhi\psout ***")
    shutil.copyfile(r'Release\CurveFile.dll', r'src\mhi\psout\CurveFile.dll')

setup(version=VERSION,
      requires=['wheel'],
      tests_require=['matplotlib'],
      package_dir={'': 'src'},
      packages=['mhi.psout'],
      ext_package='mhi.psout',
      ext_modules=[
          Extension(
              name='_psout',
              sources=['PSOut/PSOut.cpp',
                       'PSOut/Closable.cpp',
                       'PSOut/Call.cpp',
                       'PSOut/File.cpp',
                       'PSOut/Trace.cpp',
                       'PSOut/Run.cpp',
                       'PSOut/VarList.cpp',
                       ],
              include_dirs=['PSOut'],
              libraries=['CurveFile',],
              library_dirs=['Release', 'Debug', ],
              )
          ],
      package_data={
          'mhi.psout': ['*.dll'],
          },
      )
