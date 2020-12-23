# -*- mode: python ; coding: utf-8 -*-

import sys ; sys.setrecursionlimit(sys.getrecursionlimit() * 5)

block_cipher = None

added_files = [
            ( 'assets', 'assets'),
            ( 'layout', 'layout')
               ]

excludes_modules = [
            'alabaster','babel','bcrypt','cryptography','Cython','docutils','etc',
            'gevent', 'IPython','jedi','jsonschema','lib2to3','notebook','nbformat',
            'mkl','PIL','psutil','numexpr','nacl','lxml','scipy','tables','sqlalchemy',
            'tk','matplotlib','tcl','tornado','zmq'
            ]

hidden_imports = [
                ]

a = Analysis(['main.py'],
             pathex=['C:\\Users\\jjay\\Documents\\student-manager'],
             binaries=[],
             datas=added_files,
             hiddenimports=hidden_imports,
             hookspath=[],
             runtime_hooks=[],
             excludes=excludes_modules,
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='학생평가관리v1.2.2',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
