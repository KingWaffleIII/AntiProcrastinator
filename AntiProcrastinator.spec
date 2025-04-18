# -*- mode: python ; coding: utf-8 -*-


main_a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
main_pyz = PYZ(main_a.pure)
main_exe = EXE(
    main_pyz,
    main_a.scripts,
    [],
    exclude_binaries=True,
    name='AntiProcrastinator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
    contents_directory='data',
)

config_a = Analysis(
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
    optimize=0,
)
config_pyz = PYZ(config_a.pure)
config_exe = EXE(
    config_pyz,
    config_a.scripts,
    [],
    exclude_binaries=True,
    name='Configurator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
    contents_directory='data',
)

coll = COLLECT(
    main_exe,
    main_a.binaries,
    main_a.datas,
    config_exe,
    config_a.binaries,
    config_a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AntiProcrastinator',
)
