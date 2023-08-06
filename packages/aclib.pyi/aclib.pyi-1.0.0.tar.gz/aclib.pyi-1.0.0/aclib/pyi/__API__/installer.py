from __future__ import annotations

import os, time, re, glob, tempfile, traceback, PyInstaller.__main__
from distutils.dir_util import remove_tree

from .const import *
from .colorstr import *

def makeversion(dstdir, appname) -> str:
    y, m, d = (str(i) for i in time.localtime()[:3])
    mainversion = y[-2:] + m.zfill(2) + d.zfill(2)
    subversions = ['00']
    for fp in glob.glob('*', root_dir=dstdir):
        subversions += re.findall(f'^{re.escape(appname)}_{mainversion}(\d\d)(?:\.exe)?$', fp)
    subversions.sort(key=lambda v: int(v))
    subversion = str(int(subversions[-1]) + 1).zfill(2)
    return mainversion + subversion

def pyipack(
    scriptpath: str,
    distdir: str=DIR_DIST,
    appname: str=NAME_SCRIPTNAME,
    appversion: str=VER_AUTOMAKE,
    appicon: str=ICON_PYINSTALLER,   # [icopath/exepath] 可使用其他应用程序的图标
    exename: str=NAME_APPNAME,
    show_console=True,
    admin_permission=False,
    one_file_mode=False,
    appfiles: list[str]=None,    # [relaglob] 相对路径起点：scriptdir
    dst_replace_confirm=True,
):
    builddir = tempfile.TemporaryDirectory(dir='', ignore_cleanup_errors=True)
    distdir = distdir or 'dist'
    scriptdir = os.path.dirname(scriptpath)
    scriptname = os.path.basename(scriptpath)[:-3]
    appname = appname or scriptname
    appversion = appversion or makeversion(distdir, appname)
    appfullname = f'{appname}_{appversion}'
    exedir = os.path.join(distdir, appfullname)
    exename = exename or appname
    exerawpath = f'{os.path.join(exedir, appfullname)}.exe'
    exenewpath = f'{os.path.join(exedir, exename)}.exe'
    args = [scriptpath,
        f'--distpath={distdir}',
        f'--workpath={builddir.name}',
        f'--specpath={builddir.name}',
        f'--name={appfullname}',]
    for pattern in appfiles or []:
        for path in glob.glob(os.path.join(scriptdir, pattern), recursive=True):
            topath = path.replace(scriptdir, "", 1).lstrip(os.path.sep)
            topath = topath if os.path.isdir(path) else os.path.dirname(topath)
            topath = topath or "."
            datatype = "binary" if path.endswith(".pyd") else "data"
            args.append(f'--add-{datatype}={os.path.abspath(path)}{os.pathsep}{topath}')
    if appicon:
        args.append(f'--icon={appicon}')
    if not dst_replace_confirm:
        args.append('--noconfirm')
    if show_console:
        args.append('--console')
    if not show_console:
        args.append('--noconsole')
    if admin_permission:
        args.append('--uac-admin')
    if one_file_mode:
        args.append('--onefile')
    try:
        PyInstaller.__main__.run(args)
        if not one_file_mode:
            os.rename(exerawpath, exenewpath)
        print(greenstr(f'Packaged project: {os.path.abspath(exedir)}' + one_file_mode * '.exe'))
    except: traceback.print_exc()
