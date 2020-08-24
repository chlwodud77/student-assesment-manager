# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['manager.py'],
             pathex=['C:\\Users\\City\\Documents\\github\\student-manager'],
             binaries=[],
             datas=[('manager.ui','.'),('subjectInputDialog.ui','.'),('subjectStandardModify.ui','.'),('multiAssesInput.ui','.'),('setScoreFromExcel.ui','.'),('icon.ico','.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['babel','gevent','matplotlib','mpl-data','notebook','numpy','pandas','PIL','PyInstaller','scipy','sphinx','tk'],
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
          name='학생평가관리프로그램v1.2.0',
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
               name='manager')
