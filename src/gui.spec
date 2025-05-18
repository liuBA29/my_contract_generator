# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/admindell/PycharmProjects/my_contract_generator/src/main.py', '.'), ('C:/Users/admindell/PycharmProjects/my_contract_generator/src/config.py', '.'), ('C:/Users/admindell/PycharmProjects/my_contract_generator/src/create_db.py', '.'), ('C:/Users/admindell/PycharmProjects/my_contract_generator/src/database.py', '.'), ('C:/Users/admindell/PycharmProjects/my_contract_generator/src/add_customer_gui.py', '.'), ('C:/Users/admindell/PycharmProjects/my_contract_generator/src/document_generator.py', '.'), ('C:/Users/admindell/PycharmProjects/my_contract_generator/src/act_genetaror.py', '.'), ('C:/Users/admindell/PycharmProjects/my_contract_generator/src/edit_customer.py', '.'), ('C:/Users/admindell/PycharmProjects/my_contract_generator/data', 'data')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='gui',
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
    icon=['C:\\Users\\admindell\\PycharmProjects\\my_contract_generator\\src\\icon-contr.ico'],
)
