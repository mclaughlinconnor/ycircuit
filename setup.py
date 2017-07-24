# -*- coding: utf-8 -*-

# A simple setup script to create an executable using PyQt4. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# PyQt4app.py is a very simple type of PyQt4 application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

import os
import shutil
import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

includes = [
    'copy',
    'ctypes',
    'distutils',
    'io',
    'numpy',
    'numpy.core._methods',
    'numpy.lib.format',
    'os',
    'pickle',
    'platform',
    'PyQt5',
    'sip',
    'sympy',
    'src',
    'sys']

# Need to include imageformats as per
# https://stackoverflow.com/a/5722333
include_files = [
    'Resources',
    sys.prefix + '/Library/plugins/imageformats',
    sys.prefix + '/Library/plugins/platforms'
]

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
    'matplotlib',
    'multiprocessing',
    'nose',
    'PIL',
    'scipy',
    'tkinter']

options = {
    'build_exe': {
        'includes': includes,
        'excludes': excludes,
        'include_files': include_files,
        'optimize': 2
    }
}

executables = [
    Executable('top.py',
               base=base)
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
