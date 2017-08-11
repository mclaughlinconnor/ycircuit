# -*- coding: utf-8 -*-
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import os
import shutil
import sys
from cx_Freeze import setup, Executable

post = False
if 'post' in sys.argv:
    sys.argv.remove('post')
    post = True

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

includes = [
    'copy',
    'ctypes',
    'distutils',
    'io',
    'os',
    'pickle',
    'platform',
    'PyQt5',
    'sip',
    'sympy',
    'src',
    'sys']

include_files = [
    'Resources'
]

# Need to include imageformats as per
# https://stackoverflow.com/a/5722333
if sys.platform == 'win32':
    include_files.append(sys.prefix + '/Library/plugins/imageformats')
    include_files.append(sys.prefix + '/Library/plugins/platforms')
    include_files.append(sys.prefix + '/Library/bin/libeay32.dll')
    include_files.append(sys.prefix + '/Library/bin/ssleay32.dll')
if sys.platform == 'linux':
    include_files.append(sys.prefix + '/lib/x86_64-linux-gnu/qt5/plugins/imageformats')
    include_files.append(sys.prefix + '/lib/x86_64-linux-gnu/qt5/plugins/platforms')
    include_files.append(sys.prefix + '/lib/x86_64-linux-gnu/libQt5Svg.so.5')

excludes = [
    'concurrent',
    'curses',
    'email',
    'html',
    'http',
    'IPython',
    'json'
    'jupyter',
    'lib2to3',
    'lxml',
    'matplotlib',
    'mpl_toolkits',
    'multiprocessing',
    'nose',
    'numpy',
    'PIL',
    'py',
    'pydoc_data',
    'scipy',
    'tkinter',
    'urllib',
    'xml'
]

options = {
    'build_exe': {
        'includes': includes,
        'excludes': excludes,
        'include_files': include_files,
        'optimize': 2
    }
}

targetName = 'YCircuit'
if sys.platform == 'win32':
    targetName += '.exe'

executables = [
    Executable('top.py',
               base=base,
               targetName=targetName
    )
]

# Remove build directory if it exists
if os.path.isdir('build'):
    print('Removing build')
    shutil.rmtree('build')

setup(name='YCircuit',
      version='0.1',
      description='YCircuit',
      options=options,
      executables=executables
      )

# Get current branch name
from subprocess import check_output
branch = check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
# Remove newline and decode
branch = branch[:-1].decode('utf-8')

if sys.platform == 'win32':
    import zipfile
    with zipfile.ZipFile('build/ycircuit-' + branch + '_win64.zip', 'w', zipfile.ZIP_DEFLATED) as zip:
        for root, dirs, files in os.walk('build/exe.win-amd64-3.6'):
            for file in files:
                zip.write(os.path.join(root, file))
    with zipfile.ZipFile('build/ycircuit-' + branch + '_win64_update.zip', 'w', zipfile.ZIP_DEFLATED) as zip:
        for root, dirs, files in os.walk('src'):
            for file in files:
                zip.write(os.path.join(root, file))
        for root, dirs, files in os.walk('Resources'):
            for file in files:
                zip.write(os.path.join(root, file))
    if post is True:
        from subprocess import call
        call(['curl',
              '-s',
              '-u', 'siddharthshekar',
              '-X', 'POST',
              'https://api.bitbucket.org/2.0/repositories/siddharthshekar/ycircuit/downloads',
              '-F', 'files=@build/ycircuit-' + branch + '_win64.zip',
              '-F', 'files=@build/ycircuit-' + branch + '_win64_update.zip'])
if sys.platform == 'linux':
    import zipfile
    with zipfile.ZipFile('build/ycircuit-' + branch + '_linux64.zip', 'w', zipfile.ZIP_DEFLATED) as zip:
        for root, dirs, files in os.walk('build/exe.linux-x86_64-3.5'):
            for file in files:
                zip.write(os.path.join(root, file))
    with zipfile.ZipFile('build/ycircuit-' + branch + '_linux64_update.zip', 'w', zipfile.ZIP_DEFLATED) as zip:
        for root, dirs, files in os.walk('src'):
            for file in files:
                zip.write(os.path.join(root, file))
        for root, dirs, files in os.walk('Resources'):
            for file in files:
                zip.write(os.path.join(root, file))
    # import tarfile
    # with tarfile.open('build/ycircuit-' + branch + '_linux64.tar', 'w:gz') as tar:
    #     tar.add('build/exe.linux-x86_64-3.5')
    if post is True:
        from subprocess import call
        call(['curl',
              '-s',
              '-u', 'siddharthshekar',
              '-X', 'POST',
              'https://api.bitbucket.org/2.0/repositories/siddharthshekar/ycircuit/downloads',
              '-F', 'files=@build/ycircuit-' + branch + '_linux64.zip',
              '-F', 'files=@build/ycircuit-' + branch + '_linux64_update.zip'])
