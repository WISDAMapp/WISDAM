# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
import os
import sys
import importlib.metadata
import toml

specpath = os.path.dirname(os.path.abspath(SPEC))
path_to_repo_main = Path(specpath)
print("Path to repo main folder:", path_to_repo_main.as_posix())

path_to_wisdam = path_to_repo_main / "src" / "WISDAM"
sys.path.append(path_to_wisdam.as_posix())


try:
	import WISDAMcore
except ModuleNotFoundError:
	path_to_WISDAMcore = path_to_repo_main.parent / "WISDAMcore"
	if path_to_WISDAMcore.exists():
		path_to_WISDAMcore_src = path_to_WISDAMcore / "src"
		sys.path.append(path_to_WISDAMcore_src.as_posix())
	else:
		print("\nThe package WISDAMcore can not be found.\nEXIT")
		raise SystemExit

icon = path_to_wisdam / "app" / "gui_design" / "icons" / "WISDAMapp_black.ico"

pyproject_toml_file = path_to_repo_main / "pyproject.toml"

if pyproject_toml_file.exists() and pyproject_toml_file.is_file():
    toml_file = toml.load(pyproject_toml_file)
    __package_version = toml_file["project"]["version"]

name_app = 'WISDAM_' + __package_version.replace('.','_')

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
		 ( (path_to_repo_main / 'bin').as_posix(), 'bin'),
		 ( (path_to_wisdam / 'data').as_posix(), 'data'),
		 ( (path_to_wisdam / 'license').as_posix(), 'license'),
         ( (path_to_repo_main / 'docs' / 'wisdam_manual.pdf').as_posix(), '.'),
         (  pyproject_toml_file.as_posix(), '.'),
         ]

a = Analysis(
    [(path_to_wisdam / 'main.py').as_posix()],
    pathex=[path_to_repo_main.as_posix()],
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
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon.as_posix(),
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
