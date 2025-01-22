# -*- mode: python ; coding: utf-8 -*-
from kivy_deps import sdl2, glew

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('D:/Documents/Jetbrains/PycharmProjects/BingGo/img/*.png', './img')],
    # hiddenimports=['pkg_resources.py2_warn','win32timezone','six','packaging','packaging.version','webbrowser','kivy','enchant'],
    hiddenimports=['packaging','packaging.version','kivy','enchant'],
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
    [],
    exclude_binaries=True,
    name='BingGo',
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
    icon=['img_readme\\mahoupao.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    upx=True,
    upx_exclude=[],
    name='BingGo',
)
