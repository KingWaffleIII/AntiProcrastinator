# -*- mode: python ; coding: utf-8 -*-

main = Analysis(
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
main_pyz = PYZ(main.pure)
main_exe = EXE(
    main_pyz,
    main.scripts,
    main.binaries,
    main.datas,
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

configurator = Analysis(
    ['configurator.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
configurator_pyz = PYZ(configurator.pure)
configurator_exe = EXE(
    configurator_pyz,
    configurator.scripts,
    configurator.binaries,
    configurator.datas,
    [],
    name='Configurator',
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
