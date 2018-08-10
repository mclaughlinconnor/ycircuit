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

build = False
post = False
update = False
if 'build' in sys.argv:
    build = True

if 'post' in sys.argv:
    sys.argv.remove('post')
    post = True

if 'update' in sys.argv:
    sys.argv.remove('update')
    update = True

if build is True:
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
        # include_files.append(sys.prefix + '/lib/x86_64-linux-gnu/libQt5Svg.so.5')
    include_files.append('./LICENSE.txt')

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
            'zip_include_packages': [x for x in includes if x != 'src'],
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
        version='0.3',
        description='YCircuit',
        options=options,
        executables=executables
        )

# Get current branch name
from subprocess import check_output
branch = check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
# Remove newline and decode
branch = branch[:-1].decode('utf-8')
# Python version
version = str(sys.version_info[0]) + '.' + str(sys.version_info[1])

if sys.platform == 'win32':
    import zipfile
    if build is True:
        with zipfile.ZipFile('build/ycircuit-' + branch + '_win64.zip', 'w', zipfile.ZIP_DEFLATED) as zip:
            for root, dirs, files in os.walk('build/exe.win-amd64-' + version):
                for file in files:
                    zip.write(os.path.join(root, file))
    with zipfile.ZipFile('build/ycircuit-' + branch + '_win64_update.zip', 'w', zipfile.ZIP_DEFLATED) as zip:
        zip.write('build/exe.win-amd64-' + version + '/YCircuit.exe', 'YCircuit.exe')
        for root, dirs, files in os.walk('src'):
            for file in files:
                zip.write(os.path.join(root, file), 'lib/' + os.path.join(root, file))
        for root, dirs, files in os.walk('Resources'):
            for file in files:
                zip.write(os.path.join(root, file))
    if post is True:
        # Note that BB_AUTH_STRING must be set to the right value as an env variable
        from subprocess import call
        cmd = ['curl',
              '-s',
              '-u', os.environ['BB_AUTH_STRING'],
              '-X', 'POST',
              'https://api.bitbucket.org/2.0/repositories/siddharthshekar/ycircuit/downloads']
        if build is True:
            cmd += ['-F', 'files=@build/ycircuit-' + branch + '_win64.zip']
        if update is True:
            cmd += ['-F', 'files=@build/ycircuit-' + branch + '_win64_update.zip']
        call(cmd)
if sys.platform == 'linux':
    import zipfile
    if build is True:
        with zipfile.ZipFile('build/ycircuit-' + branch + '_linux64.zip', 'w', zipfile.ZIP_DEFLATED) as zip:
            for root, dirs, files in os.walk('build/exe.linux-x86_64-' + version):
                for file in files:
                    zip.write(os.path.join(root, file))
    with zipfile.ZipFile('build/ycircuit-' + branch + '_linux64_update.zip', 'w', zipfile.ZIP_DEFLATED) as zip:
        zip.write('build/exe.linux-x86_64-' + version + '/YCircuit', 'YCircuit')
        for root, dirs, files in os.walk('src'):
            for file in files:
                zip.write(os.path.join(root, file), 'lib/' + os.path.join(root, file))
        for root, dirs, files in os.walk('Resources'):
            for file in files:
                zip.write(os.path.join(root, file))
    # import tarfile
    # with tarfile.open('build/ycircuit-' + branch + '_linux64.tar', 'w:gz') as tar:
    #     tar.add('build/exe.linux-x86_64-3.5')
    if post is True:
        # Note that BB_AUTH_STRING must be set to the right value as an env variable
        from subprocess import call
        cmd = ['curl',
              '-s',
              '-u', os.environ['BB_AUTH_STRING'],
              '-X', 'POST',
              'https://api.bitbucket.org/2.0/repositories/siddharthshekar/ycircuit/downloads']
        if build is True:
            cmd += ['-F', 'files=@build/ycircuit-' + branch + '_linux64.zip']
        if update is True:
            cmd += ['-F', 'files=@build/ycircuit-' + branch + '_linux64_update.zip']
        call(cmd)
