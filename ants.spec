# -*- mode: python -*-
a = Analysis(['C:\\Users\\gw234478\\Dropbox\\ants\\ants.py'],
             pathex=['C:\\Python27\\Scripts'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
		  a.binaries + [('msvcp100.dll', 'C:\\Windows\\System32\\msvcp100.dll', 'BINARY'), ('msvcr100.dll', 'C:\\Windows\\System32\\msvcr100.dll', 'BINARY')]
		  if sys.platform == 'win32' else a.binaries,
		  a.datas + [('A.gif', 'A.gif', 'DATA'), ('ANTS.gif', 'ANTS.gif', 'DATA')],
          name='ANTS.exe',
          debug=False,
          strip=None,
          upx=True,
		  icon='A.ico',
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='ANTS')
