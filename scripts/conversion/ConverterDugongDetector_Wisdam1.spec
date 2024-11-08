# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
import os
import sys
import importlib.metadata
import toml


sys.path.append(Path(r"src\WISDAMapp").as_posix())
sys.path.append(Path(r"..\wisdamcore\src").as_posix())


src = Path(r"src\WISDAMapp")

pyproject_toml_file = Path("pyproject.toml")
if pyproject_toml_file.exists() and pyproject_toml_file.is_file():
    toml_file = toml.load(pyproject_toml_file)
    __package_version = toml_file["project"]["version"]

name_app = 'DugongDetector_to_Wisdamapp' + __package_version.replace('.','_')

block_cipher = None

rasterio_imports = ['rasterio._shim',
					'rasterio',
					'rasterio.control',
					'rasterio.crs',
					'rasterio.sample',
					'rasterio.vrt',
					'rasterio._features',
					'rasterio._base',
					'rasterio.rpc']



added_files = [
		 ( (src / 'bin').as_posix(), 'bin'),
         ( (src / 'db/conversion/project_config_dugongdetector_wisdamv1.json').as_posix(), 'bin'),
         ]

a = Analysis(
    [(src / 'db\conversion\dugongdetector_to_v1.py').as_posix()],
    pathex=['.'],
    binaries=[],
    datas=added_files,
    hiddenimports=rasterio_imports,
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
    [],
    # a.binaries,
    # a.zipfiles,
    # a.datas,
    exclude_binaries=True,
    name=name_app,
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=name_app,
)
