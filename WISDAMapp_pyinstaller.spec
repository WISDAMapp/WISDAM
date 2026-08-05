# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
import os
import shutil
import sys
import importlib.metadata
import toml

specpath = os.path.dirname(os.path.abspath(SPEC))
path_to_repo_main = Path(specpath)
print("Path to repo main folder:", path_to_repo_main.as_posix())

proj_grid_file = path_to_repo_main / "proj_dir" / "us_nga_egm08_25.tif"
if not proj_grid_file.is_file():
	raise SystemExit(
		"\nRequired PROJ grid file is missing:\n"
		f"  {proj_grid_file}\n"
		"Download us_nga_egm08_25.tif from https://cdn.proj.org/ "
		"and place it in the proj_dir folder.\n"
	)

path_to_wisdam = path_to_repo_main / "src" / "WISDAM"
sys.path.append(path_to_wisdam.as_posix())


try:
	import weitsicht
	from weitsicht import ArrayNx2
	print("import")
except (ModuleNotFoundError, ImportError):
	path_to_weitsicht = path_to_repo_main.parent / "weitsicht"
	if path_to_weitsicht.exists():
		path_to_weitsicht_src = path_to_weitsicht / "src" / "weitsicht"
		sys.path.append(path_to_weitsicht_src.as_posix())
		print(path_to_weitsicht_src)
		import weitsicht
		from weitsicht import ArrayNx2
		print("import")
	else:
		print("\nThe package weitsicht can not be found.\nEXIT")
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
					'rasterio.rpc',
					'rasterio.serde']



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

dist_app_path = Path(DISTPATH) / name_app
for folder_name in ('config', 'proj_dir'):
    source_folder = path_to_repo_main / folder_name
    target_folder = dist_app_path / folder_name
    if source_folder.exists():
        shutil.copytree(source_folder, target_folder, dirs_exist_ok=True)
