# -*- mode: python -*-

app_path = 'src'

a = Analysis([os.path.join(app_path, 'avaw.py')],
             pathex=['src'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=['PyQt4',  'django', 'Tkinter', 'win32com'])


exe_name = 'avaw'
app_icon = os.path.join(app_path, 'home/static/images/eavatar.icns')

run_strip = False
run_upx = True
console = True

if sys.platform == 'win32':
    exe_name = 'avaw.exe'
    app_icon = os.path.join(app_path, 'home/static/images/eavatar.ico')
    ext_name = '.win'
elif sys.platform.startswith('linux'):
    ext_name = '.lin'
    run_strip = True
elif sys.platform.startswith('darwin'):
    ext_name = '.mac'
    run_upx = False
    # to hide the dock icon.
    console = True
else:
    ext_name = ''


pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.dependencies,
          exclude_binaries=True,
          name=os.path.join('build', 'pyi.'+sys.platform, 'eavatar', exe_name),
          debug=False,
          strip=False,
          upx=True,
          icon=os.path.join(app_path, 'home/static/images/eavatar.ico'),
          console=console )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               Tree(os.path.join(app_path, 'home'), 'home', excludes=['*.pyc']),
               Tree(os.path.join('src', 'eavatar.ava.egg-info'), 'eavatar.ava.egg-info'),
               a.datas,
               strip=run_strip,
               upx=run_upx,
               name=os.path.join('dist', 'ava'))

if sys.platform.startswith('darwin'):
    app = BUNDLE(coll,
                name='EAvatar.app',
                appname='EAvatar',
                icon=os.path.join(app_path, 'home/static/images/eavatar.icns'))
