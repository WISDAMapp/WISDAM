# INSTALLATION

## Binary and Wheels
The latest binary and wheel can be found at https://github.com/wisdamapp/wisdam/releases/latest
There you will find a wheel which can 

### From Source
In the `WISDAM` directory (same one where you found this file after cloning the git repo), execute:
```
  pip install .
```

Testing is done using **pytest** can be found in the folder *tests*.

## Dependencies

### Python
WISDAM is tested and runs on **Python 3.10** and **Python 3.11**.

WISDAM has currently only been tested on Windows.

### Packages
WISDAM thankfully relies only on a lot of packages. The main packages are:
- [numpy](https://www.numpy.org)
- [pyproj - Python interface to proj](https://pyproj4.github.io/pyproj/stable)
- [rasterio - Easy access to geospatial raster](https://rasterio.readthedocs.io/en/stable)
- [shapely](https://shapely.readthedocs.io/en/stable/index.html)
- [QT6 with PySide6](https://doc.qt.io/qtforpython-6) under the GPLv3.
- [Pillow](https://python-pillow.org/)
- [LibRaw](https://www.libraw.org/) under the LGPLv2.1 using [rawpy](https://pypi.org/project/rawpy).
- [pandas](https://pandas.pydata.org/)
- [geopandas](https://geopandas.org/en/stable/)
- [Exiftool](https://exiftool.org/) with [PyExiftool](https://github.com/sylikc/pyexiftool) as interface to EXIFTool's command line

The source codes to comply with GPL for QT, PySide6 and LibRaw can be found at [dependecy source codes](https://github.com/WISDAMapp/dependency_source_codes) repository in the WISDAMapp GitHub project.

## Notes on PyProj
This packages heavily depends on pyproj CRS and Transformer.

## Notes on QT6 ui-Files
If you change the "ui"-Files you need to convert them to Python files.
You can use the provided batch file under "scripts".

## Building using PyInstaller
If you want to compile an executable there is a workflow for PyInstaller using the provided WISDAM_pyinstaller.spec

In the `WISDAM` directory (same one where you found this file after cloning the git repo), execute:

```pyinstaller WISDAM_pyinstaller.spec```

You need to install PyInstaller beforehand.