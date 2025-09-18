# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
import os
import sys
import importlib.metadata
import toml


specpath = Path(os.path.dirname(os.path.abspath(SPEC)))
print("Path to spec file:", specpath.as_posix())
path_to_repo_main = specpath.parent.parent
print("Path to repo main folder:", path_to_repo_main.as_posix())

path_to_src_wisdam = path_to_repo_main / "src"
path_to_wisdam = path_to_repo_main / "src" / "WISDAM"
sys.path.append(path_to_src_wisdam.as_posix())
sys.path.append(path_to_wisdam.as_posix())

try:
	from WISDAM import software_version
	print(software_version)
except (ModuleNotFoundError, ImportError):
		print("\nThe package WISDAM can not be found.\nEXIT")
		raise SystemExit

try:
	import WISDAMcore
	from WISDAMcore import ArrayNx2
	print("import")
except (ModuleNotFoundError, ImportError):
	path_to_WISDAMcore = path_to_repo_main.parent / "WISDAMcore_oldCore"
	if path_to_WISDAMcore.exists():
		path_to_WISDAMcore_src = path_to_WISDAMcore / "src" / "WISDAMcore_oldCore"
		sys.path.append(path_to_WISDAMcore_src.as_posix())
		print(path_to_WISDAMcore_src)
		import WISDAMcore
		from WISDAMcore import ArrayNx2
		print("import")
	else:
		print("\nThe package WISDAMcore can not be found.\nEXIT")
		raise SystemExit


pyproject_toml_file = path_to_repo_main / "pyproject.toml"
if pyproject_toml_file.exists() and pyproject_toml_file.is_file():
    toml_file = toml.load(pyproject_toml_file)
    __package_version = toml_file["project"]["version"]

name_app = 'DD_to_Wisdam_' + __package_version.replace('.','_')

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
         ( (specpath / 'project_config_dugongdetector.json').as_posix(), 'bin'),
         ]

a = Analysis(
    [(specpath / "dugongdetector_to_v1.py").as_posix()],
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
