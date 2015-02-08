# -*- mode: python -*-

app_path = 'src'


exe_name = 'avad'
hiddenimports = []

if sys.platform.startswith('win32'):
    exe_name = 'avad.exe'
    app_icon = os.path.join(app_path, 'res/eavatar.ico')
    ext_name = '.win'
    hiddenimports.append('depends_win32.py')
elif sys.platform.startswith('linux'):
    ext_name = '.lin'
    run_strip = True
    hiddenimports.append('depends_linux.py')
elif sys.platform.startswith('darwin'):
    ext_name = '.mac'
    hiddenimports.append('depends_osx.py')
else:
    ext_name = ''


a = Analysis([os.path.join(app_path,'avad.py')],
             pathex=['src'],
             hiddenimports=hiddenimports,
             hookspath=None,
             runtime_hooks=None,
             excludes=['PyQt4', 'wx', 'django', 'Tkinter', 'gi.repository', 'objc', 'AppKit', 'Foundation'])

run_strip = False


pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.dependencies,
          exclude_binaries=True,
          name=os.path.join('build', 'pyi.'+sys.platform, 'server', exe_name),
          debug=False,
          strip=False,
          upx=False,
          icon= os.path.join(app_path, 'home/static/images/eavatar.ico'),
          console=True )


coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               Tree(os.path.join(app_path, 'home'), 'home', excludes=['*.pyc']),
               Tree(os.path.join('src', 'eavatar.ava.egg-info'), 'eavatar.ava.egg-info'),
               a.datas,
               strip=run_strip,
               upx=True,
               name=os.path.join('dist', 'ava'))

