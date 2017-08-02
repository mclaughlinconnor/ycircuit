# -*- mode: python -*-

block_cipher = None


a = Analysis(['top.py'],
             # pathex=['/u4/sshekar/Work/ycircuit'],
             pathex=['./'],
             binaries=None,
             datas=[('Resources', './Resources')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
a.binaries = [x for x in a.binaries if not x[0].startswith('PyQt4')]
a.binaries = [x for x in a.binaries if not x[0].startswith('matplotlib')]
a.binaries = [x for x in a.binaries if not x[0].startswith('scipy')]
a.binaries = [x for x in a.binaries if not x[0].startswith('numpy')]
a.binaries = [x for x in a.binaries if not x[0].startswith('_')]
a.binaries = [x for x in a.binaries if not x[0].startswith('lib') or x[0].startswith('libpython')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='YCircuit',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='YCircuit')
