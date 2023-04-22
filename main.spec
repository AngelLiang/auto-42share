# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import platform
sys.path.append(".")
import __version__


block_cipher = None


APP_NAME = 'auto-42share' + __version__.VERSION
BUNDLE_NAME = APP_NAME + '.app'
if platform.system() == 'Windows':
    APP_NAME = 'auto-42share_win_x64-' + __version__.VERSION
    BUNDLE_NAME = APP_NAME + '.app'
elif platform.system() == 'Darwin':
    APP_NAME = 'auto-42share_mac-' + __version__.VERSION
    BUNDLE_NAME = APP_NAME + '.app'


a = Analysis(
    ['ui.py', 'main.py', 'read_csv.py', 'write_excel.py', 'config.py'],
    pathex=[os.path.join(os.getcwd())],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

app = BUNDLE(
    exe,
    name=BUNDLE_NAME,
    icon=None,
    console=False,
    debug=False,
    bundle_identifier=None,
)
