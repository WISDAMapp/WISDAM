:: You should run this in your activated python environment
pyside6-uic.exe --from-imports -o ..\src\WISDAM\app\gui_design\ui_main.py    ..\src\WISDAM\app\gui_design\gui_main.ui
pyside6-uic.exe --from-imports -o ..\src\WISDAM\app\gui_design\ui_user.py    ..\src\WISDAM\app\gui_design\gui_user.ui
pyside6-uic.exe --from-imports -o ..\src\WISDAM\app\gui_design\ui_path.py    ..\src\WISDAM\app\gui_design\gui_path.ui
pyside6-uic.exe --from-imports -o ..\src\WISDAM\app\gui_design\ui_georef.py  ..\src\WISDAM\app\gui_design\gui_georef.ui
pyside6-uic.exe --from-imports -o ..\src\WISDAM\app\gui_design\ui_meta.py    ..\src\WISDAM\app\gui_design\gui_meta.ui
pyside6-uic.exe --from-imports -o ..\src\WISDAM\app\gui_design\ui_config.py  ..\src\WISDAM\app\gui_design\gui_config.ui
pyside6-uic.exe --from-imports -o ..\src\WISDAM\app\gui_design\ui_type.py    ..\src\WISDAM\app\gui_design\gui_type.ui
pyside6-uic.exe --from-imports -o ..\src\WISDAM\app\gui_design\ui_info.py    ..\src\WISDAM\app\gui_design\gui_info.ui
pyside6-uic.exe --from-imports -o ..\src\WISDAM\app\gui_design\ui_project_creator.py ..\src\WISDAM\app\gui_design\gui_project_creator.ui
pyside6-uic.exe --from-imports -o ..\src\WISDAM\app\gui_design\ui_image_meta.py ..\src\WISDAM\app\gui_design\gui_image_meta.ui
pyside6-uic.exe --from-imports -o ..\src\WISDAM\app\gui_design\ui_mapper.py  ..\src\WISDAM\app\gui_design\gui_mapper.ui
pyside6-uic.exe --from-imports -o ..\src\WISDAM\app\gui_design\ui_about.py   ..\src\WISDAM\app\gui_design\gui_about.ui
pyside6-uic.exe --from-imports -o ..\src\WISDAM\app\gui_design\ui_confirm.py   ..\src\WISDAM\app\gui_design\gui_confirm.ui

pyside6-rcc.exe  -o ..\src\WISDAM\app\gui_design\files_rc.py ..\src\WISDAM\app\gui_design\files.qrc
