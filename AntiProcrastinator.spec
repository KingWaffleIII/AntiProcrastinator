# -*- mode: python ; coding: utf-8 -*-

import shutil

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('annoying.mp3', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AntiProcrastinator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# shutil.copyfile('config.json', '{0}/config.json'.format(DISTPATH))
# shutil.copyfile('annoying.mp3', '{0}/annoying.mp3'.format(DISTPATH))
